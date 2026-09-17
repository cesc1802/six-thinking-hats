from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import signal
import subprocess
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .oracle import HAT_PATTERNS, evaluate_case, static_validate_skill


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "cases" / "cases.json"
DEFAULT_PROFILES = ROOT / "profiles.json"
DEFAULT_SKILL = ROOT / "subject" / "six-thinking-hats"
DEFAULT_RESULTS = ROOT / "results"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe(value: str) -> str:
    return "".join(char if char.isalnum() or char in "._-" else "-" for char in value)[:80]


def _digest_tree(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(path for path in root.rglob("*") if path.is_file()):
        digest.update(str(path.relative_to(root)).encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def _run_process(command: str, args: list[str], timeout_ms: int, cwd: Path) -> dict[str, Any]:
    started = time.monotonic()
    process = subprocess.Popen(
        [command, *args],
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=timeout_ms / 1000)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(process.pid, signal.SIGTERM)
        try:
            stdout, stderr = process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
    return {
        "command": command,
        "args": args,
        "exitCode": process.returncode,
        "timedOut": timed_out,
        "durationMs": round((time.monotonic() - started) * 1000),
        "stdoutChars": len(stdout),
        "stderrChars": len(stderr),
        "stdout": stdout,
        "stderr": stderr,
    }


def classify_adapter_failure(profile: dict[str, Any], response: str, usage: Any) -> list[str]:
    failure_reasons: list[str] = []
    stripped_response = response.lstrip()
    for prefix in profile.get("failureOutputPrefixes", []):
        if stripped_response.startswith(prefix):
            failure_reasons.append(f"stdout begins with failure marker: {prefix}")
    if profile.get("requireUsage") and usage is None:
        failure_reasons.append("required usage receipt is missing")
    if isinstance(usage, dict) and (usage.get("failed") or usage.get("parseError")):
        failure_reasons.append("usage receipt reports failure or cannot be parsed")
    return failure_reasons


def run_case(
    case: dict[str, Any],
    profile_name: str,
    profile: dict[str, Any],
    output_directory: Path,
    *,
    iteration: int,
) -> dict[str, Any]:
    run_id = f"{_safe(profile_name)}-{_safe(case['id'])}-{iteration}-{uuid.uuid4().hex[:8]}"
    run_directory = output_directory / "runs" / run_id
    run_directory.mkdir(parents=True, exist_ok=False)
    usage_file = run_directory / "usage.json"
    values = {
        "prompt": case["prompt"],
        "caseId": case["id"],
        "runId": run_id,
        "usageFile": str(usage_file),
        "workspace": str(ROOT),
    }
    args = []
    for argument in profile["args"]:
        rendered = str(argument)
        for key, value in values.items():
            rendered = rendered.replace(f"{{{key}}}", str(value))
        args.append(rendered)

    execution = _run_process(
        profile["command"],
        args,
        int(profile.get("timeoutMs", 300_000)),
        ROOT,
    )
    stdout_path = run_directory / "stdout.log"
    response_path = run_directory / "response.md"
    stderr_path = run_directory / "stderr.log"
    raw_stdout = execution.pop("stdout")
    stdout_path.write_text(raw_stdout, encoding="utf-8")
    stderr_path.write_text(execution.pop("stderr"), encoding="utf-8")
    response = raw_stdout
    if profile.get("stripSessionHeader"):
        response = re.sub(r"^session_id:\s*[^\r\n]+\r?\n", "", response, count=1)
    response_path.write_text(response, encoding="utf-8")
    verification = evaluate_case(case, response)
    usage = None
    if usage_file.is_file():
        try:
            usage = json.loads(usage_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            usage = {"parseError": True}

    failure_reasons = classify_adapter_failure(profile, response, usage)
    execution["adapterFailure"] = bool(failure_reasons)
    execution["failureReasons"] = failure_reasons

    return {
        "runId": run_id,
        "caseId": case["id"],
        "suite": case.get("suite"),
        "mode": case.get("mode"),
        "profile": profile_name,
        "profileMetadata": profile.get("metadata", {}),
        "iteration": iteration,
        "execution": execution,
        "usage": usage,
        "verification": verification,
        "artifacts": {
            "stdout": str(stdout_path),
            "response": str(response_path),
            "stderr": str(stderr_path),
            "usage": str(usage_file) if usage_file.is_file() else None,
        },
    }


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_case_document(document: dict[str, Any]) -> None:
    if document.get("schemaVersion") != 1:
        raise ValueError("case document schemaVersion must be 1")
    cases = document.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("case document cases must be a non-empty array")
    seen: set[str] = set()
    valid_hats = {name for name, _ in HAT_PATTERNS}
    for index, case in enumerate(cases):
        label = f"cases[{index}]"
        if not isinstance(case, dict):
            raise ValueError(f"{label} must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            raise ValueError(f"{label}.id must be a non-empty string")
        if case_id in seen:
            raise ValueError(f"duplicate case id: {case_id}")
        seen.add(case_id)
        for field in ("prompt", "suite", "mode"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                raise ValueError(f"{label}.{field} must be a non-empty string")
        if not isinstance(case.get("profiles"), list) or not case["profiles"] or not all(
            isinstance(value, str) and value for value in case["profiles"]
        ):
            raise ValueError(f"{label}.profiles must be a non-empty string array")
        sequence = case.get("expectedHatSequence", [])
        if not isinstance(sequence, list) or any(hat not in valid_hats for hat in sequence):
            raise ValueError(f"{label}.expectedHatSequence contains an unknown hat")


def validate_profile_document(document: dict[str, Any]) -> None:
    if document.get("schemaVersion") != 1:
        raise ValueError("profile document schemaVersion must be 1")
    profiles = document.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        raise ValueError("profile document profiles must be a non-empty object")
    for name, profile in profiles.items():
        label = f"profiles.{name}"
        if not isinstance(profile, dict):
            raise ValueError(f"{label} must be an object")
        if not isinstance(profile.get("command"), str) or not profile["command"].strip():
            raise ValueError(f"{label}.command must be a non-empty executable")
        if not isinstance(profile.get("args"), list) or not all(isinstance(value, str) for value in profile["args"]):
            raise ValueError(f"{label}.args must be a string array")
        if int(profile.get("timeoutMs", 300_000)) <= 0:
            raise ValueError(f"{label}.timeoutMs must be positive")


def _select_cases(cases: list[dict[str, Any]], ids: set[str], suites: set[str]) -> list[dict[str, Any]]:
    selected = [
        case
        for case in cases
        if (not ids or case["id"] in ids) and (not suites or case.get("suite") in suites)
    ]
    if not selected:
        raise ValueError("case selectors matched no cases")
    return selected


def _summary(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    for result in results:
        group = groups.setdefault(
            result["profile"],
            {"profile": result["profile"], "runs": 0, "passed": 0, "executionFailures": 0, "durationMs": 0},
        )
        group["runs"] += 1
        group["durationMs"] += result["execution"]["durationMs"]
        execution_failed = (
            result["execution"]["timedOut"]
            or result["execution"]["exitCode"] != 0
            or result["execution"].get("adapterFailure", False)
        )
        group["executionFailures"] += int(execution_failed)
        group["passed"] += int(not execution_failed and result["verification"]["status"] == "passed")
    return [
        {
            **group,
            "passRate": group["passed"] / group["runs"] if group["runs"] else 0,
            "averageDurationMs": round(group["durationMs"] / group["runs"]) if group["runs"] else 0,
        }
        for group in groups.values()
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate the six-thinking-hats skill")
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--profiles", default=str(DEFAULT_PROFILES))
    parser.add_argument("--case", action="append", default=[])
    parser.add_argument("--suite", action="append", default=[])
    parser.add_argument("--profile", action="append", default=[])
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--jobs", type=int, default=1, help="maximum concurrent independent runs")
    parser.add_argument("--out", default=str(DEFAULT_RESULTS))
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()

    if args.repeat < 1:
        parser.error("--repeat must be at least 1")
    if args.jobs < 1:
        parser.error("--jobs must be at least 1")

    output_directory = Path(args.out).resolve()
    output_directory.mkdir(parents=True, exist_ok=True)
    case_document = _load_json(Path(args.cases))
    profile_document = _load_json(Path(args.profiles))
    validate_case_document(case_document)
    validate_profile_document(profile_document)
    profiles = profile_document["profiles"]
    referenced_profiles = {name for case in case_document["cases"] for name in case["profiles"]}
    missing_profiles = sorted(referenced_profiles - set(profiles))
    if missing_profiles:
        parser.error(f"cases reference unknown profiles: {', '.join(missing_profiles)}")
    cases = _select_cases(case_document["cases"], set(args.case), set(args.suite))
    selected_profiles = args.profile or list(profiles)
    unknown = [name for name in selected_profiles if name not in profiles]
    if unknown:
        parser.error(f"unknown profiles: {', '.join(unknown)}")

    static_result = static_validate_skill(DEFAULT_SKILL)
    started_at = _now()
    results: list[dict[str, Any]] = []
    if not args.static_only:
        tasks: list[tuple[dict[str, Any], str, dict[str, Any], int]] = []
        for profile_name in selected_profiles:
            profile = profiles[profile_name]
            for iteration in range(1, args.repeat + 1):
                for case in cases:
                    if profile_name in case.get("profiles", selected_profiles):
                        tasks.append((case, profile_name, profile, iteration))

        def execute(task: tuple[dict[str, Any], str, dict[str, Any], int]) -> dict[str, Any]:
            case, profile_name, profile, iteration = task
            print(f"[run] profile={profile_name} case={case['id']} iteration={iteration}", flush=True)
            return run_case(case, profile_name, profile, output_directory, iteration=iteration)

        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            futures = {executor.submit(execute, task): task for task in tasks}
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                print(
                    f"  profile={result['profile']} case={result['caseId']} "
                    f"execution={result['execution']['exitCode']} "
                    f"verification={result['verification']['status']} "
                    f"duration={result['execution']['durationMs']}ms",
                    flush=True,
                )
        results.sort(key=lambda item: (item["profile"], item["iteration"], item["caseId"]))

    report = {
        "schemaVersion": 1,
        "subject": {
            "id": "six-thinking-hats",
            "path": str(DEFAULT_SKILL),
            "digest": _digest_tree(DEFAULT_SKILL),
        },
        "startedAt": started_at,
        "finishedAt": _now(),
        "selection": {
            "cases": [case["id"] for case in cases],
            "profiles": selected_profiles,
            "repeat": args.repeat,
            "jobs": args.jobs,
        },
        "staticValidation": static_result,
        "results": results,
        "summary": _summary(results),
    }
    report_path = output_directory / f"report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"static": static_result["status"], "summary": report["summary"], "report": str(report_path)}, ensure_ascii=False, indent=2))

    failed = static_result["status"] != "passed" or any(
        result["execution"]["timedOut"]
        or result["execution"]["exitCode"] != 0
        or result["execution"].get("adapterFailure", False)
        or result["verification"]["status"] != "passed"
        for result in results
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

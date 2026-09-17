from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .oracle import evaluate_case
from .runner import (
    DEFAULT_CASES,
    DEFAULT_PROFILES,
    _summary,
    classify_adapter_failure,
    validate_case_document,
    validate_profile_document,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Regrade stored responses without rerunning the agent")
    parser.add_argument("report")
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--profiles", default=str(DEFAULT_PROFILES))
    parser.add_argument("--out")
    args = parser.parse_args()

    report_path = Path(args.report).resolve()
    report = json.loads(report_path.read_text(encoding="utf-8"))
    case_document = json.loads(Path(args.cases).read_text(encoding="utf-8"))
    profile_document = json.loads(Path(args.profiles).read_text(encoding="utf-8"))
    validate_case_document(case_document)
    validate_profile_document(profile_document)
    cases = {case["id"]: case for case in case_document["cases"]}
    profiles = profile_document["profiles"]

    for result in report["results"]:
        case = cases[result["caseId"]]
        profile = profiles[result["profile"]]
        response_artifact = result["artifacts"].get("response") or result["artifacts"]["stdout"]
        response = Path(response_artifact).read_text(encoding="utf-8")
        result["verification"] = evaluate_case(case, response)
        reasons = classify_adapter_failure(profile, response, result.get("usage"))
        result["execution"]["adapterFailure"] = bool(reasons)
        result["execution"]["failureReasons"] = reasons

    report["regradedAt"] = datetime.now(timezone.utc).isoformat()
    report["regradedFrom"] = str(report_path)
    report["summary"] = _summary(report["results"])
    out = Path(args.out).resolve() if args.out else report_path.with_name(report_path.stem + "-regraded.json")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"summary": report["summary"], "report": str(out)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

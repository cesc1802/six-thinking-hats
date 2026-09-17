from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


HAT_PATTERNS = [
    ("blue", re.compile(r"(?:🔵|\bblue\b|mũ\s+xanh\s+(?:lam|dương))", re.I)),
    ("white", re.compile(r"(?:⚪|\bwhite\b|mũ\s+trắng)", re.I)),
    ("red", re.compile(r"(?:🔴|\bred\b|mũ\s+đỏ)", re.I)),
    ("yellow", re.compile(r"(?:🟡|\byellow\b|mũ\s+vàng)", re.I)),
    ("black", re.compile(r"(?:⚫|\bblack\b|mũ\s+đen)", re.I)),
    ("green", re.compile(r"(?:🟢|\bgreen\b|mũ\s+xanh\s+lá)", re.I)),
]

HAT_START_PATTERNS = [
    ("blue", re.compile(r"^(?:🔵\s*)?(?:mũ\s+xanh\s+(?:lam|dương)|blue(?:\s+hat)?)(?:\b|\s|[-—:])", re.I)),
    ("white", re.compile(r"^(?:⚪\s*)?(?:mũ\s+trắng|white(?:\s+hat)?)(?:\b|\s|[-—:])", re.I)),
    ("red", re.compile(r"^(?:🔴\s*)?(?:mũ\s+đỏ|red(?:\s+hat)?)(?:\b|\s|[-—:])", re.I)),
    ("yellow", re.compile(r"^(?:🟡\s*)?(?:mũ\s+vàng|yellow(?:\s+hat)?)(?:\b|\s|[-—:])", re.I)),
    ("black", re.compile(r"^(?:⚫\s*)?(?:mũ\s+đen|black(?:\s+hat)?)(?:\b|\s|[-—:])", re.I)),
    ("green", re.compile(r"^(?:🟢\s*)?(?:mũ\s+xanh\s+lá|green(?:\s+hat)?)(?:\b|\s|[-—:])", re.I)),
]


def _check(oracle: str, passed: bool, expected: Any, actual: Any) -> dict[str, Any]:
    return {
        "oracle": oracle,
        "status": "passed" if passed else "failed",
        "expected": expected,
        "actual": actual,
    }


def _line_hat(line: str, *, allow_table: bool) -> str | None:
    stripped = line.strip()
    # Prefer true section headings. Table rows are accepted only as a fallback
    # for quick-mode outputs that intentionally collapse all hats into a table.
    is_heading = stripped.startswith("#")
    is_table_row = allow_table and stripped.startswith("|") and stripped.endswith("|")
    is_bold_heading = stripped.startswith("**") and stripped.count("**") >= 2
    if not (is_heading or is_table_row or is_bold_heading):
        return None
    if is_table_row:
        candidates = [cell.strip() for cell in stripped.strip("|").split("|")]
    elif is_heading:
        candidates = [re.sub(r"^#+\s*", "", stripped)]
    else:
        candidates = [stripped.removeprefix("**").strip()]
    for content in candidates:
        for name, pattern in HAT_START_PATTERNS:
            if pattern.search(content):
                return name
    return None


def _sequence_with_mode(text: str) -> tuple[list[str], bool]:
    heading_sequence = [
        hat for line in text.splitlines() if (hat := _line_hat(line, allow_table=False)) is not None
    ]
    if heading_sequence:
        return heading_sequence, False
    table_sequence = [
        hat for line in text.splitlines() if (hat := _line_hat(line, allow_table=True)) is not None
    ]
    return table_sequence, True


def parse_hat_sequence(text: str) -> list[str]:
    sequence, _ = _sequence_with_mode(text)
    return sequence


def _hat_sections(text: str) -> list[tuple[str, str]]:
    _, allow_table = _sequence_with_mode(text)
    sections: list[tuple[str, list[str]]] = []
    for line in text.splitlines():
        hat = _line_hat(line, allow_table=allow_table)
        if hat:
            sections.append((hat, []))
        elif sections:
            sections[-1][1].append(line)
    return [(hat, "\n".join(lines).strip()) for hat, lines in sections]


def _count_green_ideas(text: str) -> int:
    sections = _hat_sections(text)
    green = next((body for hat, body in sections if hat == "green"), "")
    numbered = re.findall(r"(?im)^\s*(?:[-*]\s*)?(?:G\d+|\d+[.)])\s*[:.)-]?\s*\S+", green)
    if numbered:
        return len(numbered)
    return len(re.findall(r"(?m)^\s*[-*]\s+\S+", green))


def _first_red_sentence_count(text: str) -> int:
    red = next((body for hat, body in _hat_sections(text) if hat == "red"), "")
    if not red:
        return 0
    plain = re.sub(r"(?m)^\s*[-*]\s*", "", red).strip()
    return len([part for part in re.split(r"(?<=[.!?])\s+|\n+", plain) if part.strip()])


def _question_count(text: str) -> int:
    return text.count("?")


def _language_check(text: str, language: str) -> tuple[bool, Any]:
    if language == "vi":
        markers = re.findall(r"[ăâđêôơưáàảãạéèẻẽẹíìỉĩịóòỏõọúùủũụýỳỷỹỵ]", text, re.I)
        return len(markers) >= 3, {"vietnamese_diacritics": len(markers)}
    if language == "en":
        letters = [char for char in text if char.isalpha()]
        ascii_letters = [char for char in letters if char.isascii()]
        ratio = len(ascii_letters) / len(letters) if letters else 0
        return ratio >= 0.9, {"ascii_letter_ratio": round(ratio, 3)}
    return True, {"language": language, "checked": False}


def evaluate_case(case: dict[str, Any], response: str) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    sequence = parse_hat_sequence(response)

    if "expectedHatSequence" in case:
        expected = case["expectedHatSequence"]
        checks.append(_check("hat.sequence", sequence == expected, expected, sequence))

    if "allowedHats" in case:
        allowed = set(case["allowedHats"])
        unexpected = [hat for hat in sequence if hat not in allowed]
        checks.append(_check("hat.allowed", not unexpected, sorted(allowed), unexpected))

    for value in case.get("required", []):
        checks.append(_check("text.contains", value.casefold() in response.casefold(), value, None))

    for alternatives in case.get("requiredAny", []):
        found = [value for value in alternatives if value.casefold() in response.casefold()]
        checks.append(_check("text.contains-any", bool(found), alternatives, found))

    for value in case.get("forbidden", []):
        checks.append(_check("text.not-contains", value.casefold() not in response.casefold(), value, None))

    if "minGreenIdeas" in case:
        count = _count_green_ideas(response)
        checks.append(_check("green.min-ideas", count >= case["minGreenIdeas"], case["minGreenIdeas"], count))

    if "maxRedFirstSentences" in case:
        count = _first_red_sentence_count(response)
        checks.append(_check("red.max-sentences", 0 < count <= case["maxRedFirstSentences"], case["maxRedFirstSentences"], count))

    if "expectedQuestionCount" in case:
        count = _question_count(response)
        checks.append(_check("response.question-count", count == case["expectedQuestionCount"], case["expectedQuestionCount"], count))

    if "maxHatOccurrences" in case:
        checks.append(_check("hat.max-occurrences", len(sequence) <= case["maxHatOccurrences"], case["maxHatOccurrences"], len(sequence)))

    if "maxChars" in case:
        checks.append(_check("response.max-chars", len(response) <= case["maxChars"], case["maxChars"], len(response)))

    if case.get("language"):
        passed, actual = _language_check(response, case["language"])
        checks.append(_check("response.language", passed, case["language"], actual))

    failed = sum(check["status"] == "failed" for check in checks)
    return {
        "caseId": case.get("id"),
        "status": "failed" if failed else "passed",
        "summary": {"passed": len(checks) - failed, "failed": failed, "total": len(checks)},
        "hatSequence": sequence,
        "checks": checks,
    }


def _frontmatter(content: str) -> tuple[dict[str, Any], str]:
    if not content.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = content.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed")
    raw = content[4:end]
    values: dict[str, Any] = {}
    for line in raw.splitlines():
        if not line.strip() or line[:1].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if key == "metadata" and value:
            try:
                values[key] = json.loads(value)
            except json.JSONDecodeError:
                values[key] = value
        else:
            values[key] = value.strip('"\'')
    return values, content[end + 5 :]


def static_validate_skill(skill_dir: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    skill_file = skill_dir / "SKILL.md"
    checks.append(_check("skill.file-exists", skill_file.is_file(), "SKILL.md", str(skill_file)))
    if not skill_file.is_file():
        return {"status": "failed", "summary": {"passed": 0, "failed": 1, "total": 1}, "checks": checks}

    content = skill_file.read_text(encoding="utf-8")
    try:
        metadata, body = _frontmatter(content)
        fm_ok = True
        fm_actual: Any = sorted(metadata)
    except ValueError as error:
        metadata, body = {}, ""
        fm_ok = False
        fm_actual = str(error)
    checks.append(_check("skill.frontmatter", fm_ok, "valid frontmatter", fm_actual))

    name = metadata.get("name", "")
    checks.append(_check("skill.name", bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)), "lowercase kebab-case", name))
    description = metadata.get("description", "")
    checks.append(_check("skill.description", bool(description) and len(description) <= 1024, "1..1024 chars", len(description)))
    checks.append(_check("skill.body", bool(body.strip()), "non-empty", len(body.strip())))
    checks.append(_check("skill.size", len(content) <= 100_000, "<=100000 chars", len(content)))

    referenced = sorted(set(re.findall(r"`((?:references|assets)/[^`\s]+)`", body)))
    missing = [path for path in referenced if not (skill_dir / path).is_file()]
    checks.append(_check("skill.references", not missing, referenced, {"missing": missing}))

    expected_files = [
        "references/hats.md",
        "references/sequences.md",
        "references/example-x-technology.md",
        "assets/report-template.md",
    ]
    absent = [path for path in expected_files if not (skill_dir / path).is_file()]
    checks.append(_check("skill.package-files", not absent, expected_files, {"missing": absent}))

    failed = sum(check["status"] == "failed" for check in checks)
    return {
        "status": "failed" if failed else "passed",
        "summary": {"passed": len(checks) - failed, "failed": failed, "total": len(checks)},
        "checks": checks,
    }

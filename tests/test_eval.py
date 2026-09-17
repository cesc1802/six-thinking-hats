import json
import tempfile
import unittest
from pathlib import Path

from evals.oracle import evaluate_case, parse_hat_sequence, static_validate_skill


ROOT = Path(__file__).resolve().parents[1]


class OracleTests(unittest.TestCase):
    def test_parses_vietnamese_and_english_hat_headings(self):
        text = """
## 🔵 Mũ xanh lam — mở đầu
## ⚪ White — facts
## 🔴 Mũ đỏ
## 🟡 Yellow
## ⚫ Mũ đen
## 🟢 Green
## 🔴 Red — check
## 🔵 Blue — close
"""
        self.assertEqual(
            parse_hat_sequence(text),
            ["blue", "white", "red", "yellow", "black", "green", "red", "blue"],
        )

    def test_prefers_executed_headings_over_agenda_table(self):
        text = """
| Mũ | Mục đích |
|---|---|
| 🔵 Mũ xanh dương | mở |
| ⚪ Mũ trắng | facts |
## 🔵 Mũ xanh dương — mở đầu
## ⚪ Mũ trắng — facts
## 🔵 Mũ xanh dương — kết luận
"""
        self.assertEqual(parse_hat_sequence(text), ["blue", "white", "blue"])

    def test_uses_hat_column_when_quick_mode_is_a_table(self):
        text = """
| Time | Hat | Goal |
|---|---|---|
| 00:00 | Mũ xanh lam | open |
| 05:00 | Mũ trắng | facts |
| 10:00 | Mũ xanh lam | close |
"""
        self.assertEqual(parse_hat_sequence(text), ["blue", "white", "blue"])

    def test_ignores_declared_sequence_and_nested_hat_mentions(self):
        text = """
# Mũ xanh lam — mở
**Trình tự:** Mũ xanh lam → Mũ trắng → Mũ đen
# Mũ đen — rủi ro
### Phán quyết Mũ đen
"""
        self.assertEqual(parse_hat_sequence(text), ["blue", "black"])

    def test_detects_missing_blue_open_and_wrong_order(self):
        case = {
            "id": "quick",
            "expectedHatSequence": ["blue", "white", "red", "yellow", "black", "green", "red", "blue"],
        }
        response = """
| ⚪ White | facts |
| 🔴 Red | feeling |
| ⚫ Black | risk |
| 🟡 Yellow | value |
| 🟢 Green | ideas |
| 🔵 Blue | decision |
"""
        result = evaluate_case(case, response)
        self.assertEqual(result["status"], "failed")
        sequence_check = next(c for c in result["checks"] if c["oracle"] == "hat.sequence")
        self.assertEqual(sequence_check["status"], "failed")

    def test_compliant_full_response_passes(self):
        case = {
            "id": "full",
            "expectedHatSequence": ["blue", "white", "red", "yellow", "black", "green", "red", "blue"],
            "required": ["Option 0", "[FACT:", "[NEED-DATA:", "Khuyến nghị"],
            "requiredAny": [["Owner", "Chủ trì"]],
            "minGreenIdeas": 3,
        }
        response = """
## 🔵 Mũ xanh lam — mở đầu
Option 0: giữ nguyên. Mode full.
## ⚪ Mũ trắng
[FACT: user prompt] Dữ kiện. [NEED-DATA: đo thêm]
## 🔴 Mũ đỏ — lần đầu
Trực giác thấy rủi ro.
## 🟡 Mũ vàng
Lợi ích ngắn, trung và dài hạn.
## ⚫ Mũ đen
Rủi ro có cơ chế và tác động.
## 🟢 Mũ xanh lá
- G1: thử nhỏ
- G2: triển khai theo pha
- G3: bỏ ràng buộc
## 🔴 Mũ đỏ — kiểm tra lại
Cảm nhận đã thay đổi.
## 🔵 Mũ xanh lam — kết luận
Khuyến nghị: thử nhỏ. Owner: Tech Lead.
"""
        result = evaluate_case(case, response)
        self.assertEqual(result["status"], "passed", result)

    def test_static_validation_accepts_supplied_skill(self):
        result = static_validate_skill(ROOT)
        self.assertEqual(result["status"], "passed", result)
        self.assertGreaterEqual(result["summary"]["passed"], 6)

    def test_static_validation_fails_missing_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "SKILL.md").write_text(
                "---\nname: example\ndescription: Use when testing.\n---\nBody references `references/missing.md`.\n",
                encoding="utf-8",
            )
            result = static_validate_skill(root)
            self.assertEqual(result["status"], "failed")
            self.assertTrue(any(c["oracle"] == "skill.references" and c["status"] == "failed" for c in result["checks"]))


if __name__ == "__main__":
    unittest.main()

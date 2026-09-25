"""Tests for repository zero-emoji invariant scanner."""

import sys
import tempfile
import unittest
from pathlib import Path

# Add repo root to path to import bin/check_no_emojis.py
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "bin"))
import check_no_emojis  # noqa: E402


class TestNoEmojisScanner(unittest.TestCase):
    """Test suite for emoji detection and cuneiform discrimination."""

    def test_cuneiform_signs_not_flagged_as_emojis(self):
        """Legitimate ancient cuneiform Unicode signs must never trigger emoji violations."""
        cuneiform_samples = [
            "𒂊𒁹",      # e-dish
            "𒁾𒊬",    # dub-sar
            "𒅗𒁹",      # ka-dish
            "𒁀𒋛",      # ba-si
            "𒈬𒁶",      # mu-gim
            "𒇽",        # lu2
            "𒀭𒂗𒆠",     # dingir-en-ki
            "365;14,31,55 𒌓",
        ]
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
            for s in cuneiform_samples:
                f.write(s + "\n")
            f_path = Path(f.name)

        try:
            findings = check_no_emojis.check_file(f_path)
            self.assertEqual(len(findings), 0, f"False positives on cuneiform: {findings}")
        finally:
            f_path.unlink()

    def test_disallowed_emojis_detected(self):
        """Standard Unicode emojis must be detected and reported."""
        emoji_samples = [
            ("\U0001F680", "Rocket emoji"),
            ("\U0001F389", "Party popper"),
            ("\U0001F916", "Robot face"),
            ("\u2728", "Sparkles"),
            ("\U0001F44D", "Thumbs up"),
            ("\U0001F525", "Fire"),
        ]
        for emoji_char, desc in emoji_samples:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
                f.write(f"Line with {emoji_char} ({desc})\n")
                f_path = Path(f.name)

            try:
                findings = check_no_emojis.check_file(f_path)
                self.assertGreater(len(findings), 0, f"Failed to detect {desc}")
                self.assertEqual(findings[0][1], emoji_char)
            finally:
                f_path.unlink()

    def test_clean_file_passes(self):
        """Standard plain text, numbers, punctuation, and code must pass without violations."""
        clean_text = """# Clean DUB.SAR program
problem
    a : 10
    b : 20
    c := a + b
result
    output "sum:"
    output c
"""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
            f.write(clean_text)
            f_path = Path(f.name)

        try:
            findings = check_no_emojis.check_file(f_path)
            self.assertEqual(len(findings), 0)
        finally:
            f_path.unlink()


if __name__ == "__main__":
    unittest.main()

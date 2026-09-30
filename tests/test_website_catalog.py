"""Catalog metadata used by the website, read from examples/*.dub."""

import importlib.util
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PREPARE_ASSETS = REPO_ROOT / "website" / "scripts" / "prepare_assets.py"


def _load_prepare_assets():
    spec = importlib.util.spec_from_file_location("prepare_assets", PREPARE_ASSETS)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {PREPARE_ASSETS}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WebsiteCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = {
            entry["id"]: entry
            for entry in _load_prepare_assets().build_catalog(REPO_ROOT / "examples")
        }

    def test_first_tablet_scholar_is_beginner_scholar(self):
        entry = self.catalog["first_tablet_scholar"]
        self.assertEqual(entry["difficulty"], "beginner")
        self.assertEqual(entry["mode"], "scholar")
        self.assertIn("problem section", entry["purpose"])
        self.assertIn("problem", entry["source"])

    def test_reciprocal_lookup_is_tablet_mastery(self):
        entry = self.catalog["reciprocal_lookup"]
        self.assertEqual(entry["mode"], "tablet")
        self.assertEqual(entry["difficulty"], "mastery")

    def test_first_tablet_is_mixed(self):
        self.assertEqual(self.catalog["first_tablet"]["mode"], "mixed")

    def test_every_example_has_source(self):
        self.assertGreaterEqual(len(self.catalog), 40)
        for entry in self.catalog.values():
            self.assertTrue(entry["source"].strip())
            self.assertIn(entry["mode"], {"scholar", "tablet", "mixed"})


if __name__ == "__main__":
    unittest.main()

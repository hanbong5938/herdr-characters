"""Regression coverage for manifest-discovered gallery records."""

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from catalog_inventory import synchronize_catalog


class CatalogInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "packs").mkdir()
        self.previews = self.root / "stage/previews"
        self.catalog = {
            "schemaVersion": 1,
            "repositoryUrl": "https://github.com/example/characters",
            "submissionUrl": "https://github.com/example/characters/issues",
            "releaseTag": "packs-v0.0.2",
            "characters": [],
        }

    def add_png_pack(self, directory, identifier, name="Mika", frame="idle.png"):
        pack = self.root / "packs" / directory
        pack.mkdir()
        (pack / "LICENSE.txt").write_text("Source terms")
        Image.new("RGBA", (800, 600), (21, 72, 193, 128)).save(pack / "idle.png")
        (pack / "entry.json").write_text(json.dumps({"phases": {"idle": {"frames": [frame]}}}))
        (pack / "manifest.json").write_text(json.dumps({
            "format": "herdr.character", "version": 4, "id": identifier,
            "name": name, "author": {"name": "Maker"}, "render_mode": "png",
            "entry": "entry.json", "licenses": [{"expression": "MIT", "path": "LICENSE.txt"}],
        }))
        return pack

    def sync(self):
        return synchronize_catalog(self.root, self.catalog, self.previews)

    def test_unlisted_pack_has_real_preview_and_manifest_metadata(self):
        self.add_png_pack("mika-files", "mika", "미카")
        result = self.sync()
        item = result["characters"][0]
        self.assertEqual(item["name"], "미카")
        self.assertEqual(item["author"], "Maker")
        self.assertEqual(item["sourceUrl"], "https://github.com/example/characters/tree/main/packs/mika-files")
        self.assertEqual(item["license"], {"label": "MIT", "path": "packs/mika-files/LICENSE.txt"})
        self.assertIsNone(item["publishedAt"])
        self.assertIn("미카", item["tags"])
        self.assertNotIn("variants", item)
        self.assertNotIn("download", item)
        with Image.open(self.previews / "mika-source.png") as preview:
            self.assertEqual(preview.format, "PNG")
            self.assertEqual(preview.mode, "RGBA")
            self.assertEqual(preview.size, (512, 384))
            red, green, blue, alpha = preview.getpixel((250, 180))
            self.assertGreater(blue, red)
            self.assertGreater(blue, green)
            self.assertGreater(alpha, 0)
            self.assertLess(alpha, 255)
        self.assertFalse((self.root / item["profile"]).exists())

    def test_published_metadata_and_curated_research_profile_survive(self):
        self.add_png_pack("png-example", "coding-cat", "Coding Cat")
        self.add_png_pack("arin-research", "arin-research", "아린")
        (self.root / "previews").mkdir()
        Image.new("RGBA", (32, 32), (253, 1, 2, 255)).save(self.root / "previews/arin-profile.png")
        authored = {
            "id": "arin-research", "type": "research", "name": "Arin",
            "displayName": {"en": "Arin", "ko": "아린"}, "author": "Research author",
            "description": {"en": "Authored profile", "ko": "원본 설명"}, "tags": ["arin"],
            "publishedAt": "2026-10-08", "profile": "previews/arin-profile.png",
            "sourceUrl": "https://example.com/arin",
            "license": {"label": "Research", "displayLabel": {"en": "Research", "ko": "연구"},
                        "path": "packs/arin-research/LICENSE.txt"},
        }
        (self.root / "catalog.source.json").write_text(json.dumps({"characters": [
            authored,
            {"id": "coding-cat", "type": "pack",
             "displayName": {"en": "Wrong source", "ko": "잘못된 원본"},
             "variants": [{"id": "coding-cat", "licenseDisplayLabel": {"en": "Wrong source", "ko": "잘못된 원본"}}]},
        ]}))
        original = {
            "id": "coding-cat", "name": "Coding Cat", "type": "pack", "author": "Herdr contributors",
            "displayName": {"en": "Coding Cat", "ko": "코딩 캣"},
            "description": {"en": "Published", "ko": "출시"}, "tags": ["cat"],
            "variants": [{"id": "coding-cat", "version": "0.0.2", "publishedAt": "2026-10-06",
                          "download": {"path": "downloads/cat.herdrchar", "bytes": 421, "sha256": "f" * 64},
                          "preview": {"idle": "previews/cat.png", "running": []},
                          "license": {"label": "MIT", "displayLabel": {"en": "MIT", "ko": "MIT"},
                                      "path": "packs/png-example/LICENSE.txt"}}],
        }
        self.catalog["characters"] = [original, {
            "id": "arin-research", "type": "research", "name": "Stale",
            "displayName": {"en": "Stale", "ko": "오래된 이름"},
            "license": {"label": "Old terms", "displayLabel": {"en": "Old", "ko": "이전"}},
        }]
        characters = {item["id"]: item for item in self.sync()["characters"]}
        self.assertEqual(characters["coding-cat"], original)
        self.assertEqual(characters["arin-research"]["description"], authored["description"])
        self.assertEqual(characters["arin-research"]["profile"], authored["profile"])
        self.assertEqual(characters["arin-research"]["displayName"], authored["displayName"])
        self.assertEqual(characters["arin-research"]["license"], authored["license"])
        self.assertNotIn("sourceTerms", characters["arin-research"])
        self.assertFalse((self.previews / "arin-research-source.png").exists())

    def test_rig_initial_psd_produces_png_with_recorded_approval_date(self):
        fixture = ROOT / "packs/rubelia-school-uniform/waiting.psd"
        pack = self.root / "packs" / "new-rig"
        pack.mkdir()
        shutil.copyfile(fixture, pack / "first.psd")
        (pack / "LICENSE.txt").write_text("Source terms")
        (pack / "rig-entry.json").write_text(json.dumps({"initial": "waiting", "models": [
            {"id": "other", "file": "missing.psd"}, {"id": "waiting", "file": "first.psd"}]}))
        (pack / "manifest.json").write_text(json.dumps({
            "format": "herdr.character", "version": 5, "id": "new-rig", "name": "루벨리아(교복)",
            "author": {"name": "Artist"}, "render_mode": "rig", "entry": "rig-entry.json",
            "licenses": [{"expression": "Research", "path": "LICENSE.txt"}],
        }))
        (pack / "owner-approval.json").write_text(json.dumps({
            "wardrobeRepositorySourceApproval": {"approved": True, "date": "2026-10-08"}}))
        item = self.sync()["characters"][0]
        self.assertEqual(item["publishedAt"], "2026-10-08")
        self.assertEqual(item["name"], "루벨리아(교복)")
        with Image.open(self.previews / "new-rig-source.png") as preview:
            self.assertEqual(preview.format, "PNG")
            self.assertEqual(preview.size, (512, 512))
            self.assertEqual(preview.mode, "RGBA")
            self.assertGreater(preview.getchannel("A").getextrema()[1], 0)
        self.assertFalse((self.previews / "first.psd").exists())

    def test_new_source_pack_does_not_add_a_downloadable_variant(self):
        self.add_png_pack("published", "published")
        self.add_png_pack("new-source", "new-source", "New artwork")
        published = {
            "id": "published", "type": "pack", "name": "Published",
            "variants": [{"id": "published", "download": {"sha256": "a" * 64}}],
        }
        self.catalog["characters"] = [published]
        result = self.sync()
        self.assertEqual([item["id"] for item in result["characters"]], ["published", "new-source"])
        self.assertEqual(result["characters"][0], published)
        self.assertEqual(result["characters"][1]["type"], "research")
        self.assertEqual(result["characters"][1]["name"], "New artwork")
        self.assertEqual(result["characters"][1]["profile"], "previews/new-source-source.png")
        with Image.open(self.previews / "new-source-source.png") as preview:
            self.assertEqual(preview.format, "PNG")
        self.assertEqual(sum(len(item["variants"]) for item in result["characters"] if item["type"] == "pack"), 1)

    def test_published_group_represents_distinct_variant_manifests(self):
        self.add_png_pack("summer-files", "wardrobe-summer", "Summer")
        self.add_png_pack("winter-files", "wardrobe-winter", "Winter")
        self.add_png_pack("additional-files", "new-pack", "Additional")
        published = {
            "id": "wardrobe", "type": "pack", "name": "Wardrobe",
            "description": {"en": "Curated group"}, "tags": ["outfits"],
            "variants": [
                {"id": "wardrobe-summer", "download": {"sha256": "a" * 64}, "version": "1.0"},
                {"id": "wardrobe-winter", "download": {"sha256": "b" * 64}, "version": "2.0"},
            ],
        }
        self.catalog["characters"] = [published]
        (self.root / "catalog.source.json").write_text(json.dumps({
            "characters": [{"id": "wardrobe", "type": "pack"}],
        }))
        characters = self.sync()["characters"]
        self.assertEqual([item["id"] for item in characters], ["wardrobe", "new-pack"])
        self.assertEqual(characters[0], published)
        self.assertEqual(characters[0]["variants"], published["variants"])
        self.assertEqual(characters[1]["type"], "research")
        self.assertTrue((self.previews / "new-pack-source.png").is_file())
        self.assertFalse((self.previews / "wardrobe-summer-source.png").exists())
        self.assertFalse((self.previews / "wardrobe-winter-source.png").exists())

    def test_duplicate_or_missing_published_variant_reports_identity(self):
        self.add_png_pack("summer", "wardrobe-summer")
        self.catalog["characters"] = [
            {"id": "wardrobe", "type": "pack", "variants": [
                {"id": "wardrobe-summer"}, {"id": "wardrobe-summer"}]},
        ]
        with self.assertRaises(ValueError) as duplicate:
            self.sync()
        self.assertIn("wardrobe-summer", str(duplicate.exception))
        self.catalog["characters"][0]["variants"][1]["id"] = "wardrobe-winter"
        with self.assertRaises(ValueError) as missing:
            self.sync()
        self.assertIn("wardrobe-winter", str(missing.exception))

    def test_duplicate_and_missing_declared_source_fail_with_paths(self):
        self.add_png_pack("first", "shared")
        second = self.add_png_pack("second", "shared")
        with self.assertRaisesRegex(ValueError, r"second/manifest\.json"):
            self.sync()
        (second / "manifest.json").unlink()
        with self.assertRaisesRegex(ValueError, r"second/manifest\.json"):
            self.sync()
        shutil.rmtree(second)
        first = self.root / "packs/first"
        (first / "entry.json").write_text(json.dumps({"phases": {"idle": {"frames": ["gone.png"]}}}))
        with self.assertRaisesRegex(ValueError, r"gone\.png"):
            self.sync()
        (first / "manifest.json").write_text("{broken")
        with self.assertRaisesRegex(ValueError, r"first/manifest\.json"):
            self.sync()
        shutil.rmtree(first)
        self.add_png_pack("third", "third")
        third = self.root / "packs/third"
        manifest = json.loads((third / "manifest.json").read_text())
        manifest["licenses"] = []
        (third / "manifest.json").write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, r"third/manifest\.json"):
            self.sync()
        manifest["licenses"] = [{"expression": "MIT", "path": "LICENSE.txt"}]
        manifest["render_mode"] = "unsupported"
        (third / "manifest.json").write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, r"third/manifest\.json"):
            self.sync()

    def test_discovered_records_are_rebuilt_after_rename_or_removal(self):
        pack = self.add_png_pack("mika", "mika", "Mika")
        old = self.sync()["characters"][0]
        old["displayName"] = {"en": "Old", "ko": "이전"}
        old["license"]["displayLabel"] = {"en": "Old terms", "ko": "이전 조건"}
        self.catalog["characters"] = [old]
        manifest = json.loads((pack / "manifest.json").read_text())
        manifest["name"] = "새 이름"
        manifest["licenses"][0]["expression"] = "New terms"
        (pack / "manifest.json").write_text(json.dumps(manifest))
        changed = self.sync()["characters"][0]
        self.assertEqual(changed["name"], "새 이름")
        self.assertEqual(changed["profile"], "previews/mika-source.png")
        self.assertNotEqual(changed["description"], old["description"])
        self.assertEqual(changed["license"]["label"], "New terms")
        self.assertNotIn("displayName", changed)
        self.assertNotIn("displayLabel", changed["license"])
        shutil.rmtree(pack)
        self.assertEqual(self.sync()["characters"], [])
        self.add_png_pack("replacement", "new-id", "New")
        self.assertEqual([item["id"] for item in self.sync()["characters"]], ["new-id"])


if __name__ == "__main__":
    unittest.main()

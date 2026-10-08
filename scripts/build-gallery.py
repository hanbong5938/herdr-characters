#!/usr/bin/env python3
"""Stage only gallery files, pack notices, previews, and verified downloads."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
from catalog_inventory import synchronize_catalog

ROOT = Path(__file__).resolve().parents[1]


def main():
    source_catalog = json.loads((ROOT / "catalog.json").read_text())
    output = ROOT / "dist/gallery"
    output.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="gallery-", dir=output.parent) as temporary:
        stage = Path(temporary)
        (stage / "previews").mkdir()
        catalog = synchronize_catalog(ROOT, source_catalog, stage / "previews")
        for name in ("index.html", "app.js", "styles.css"):
            shutil.copyfile(ROOT / name, stage / name)
        (stage / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
        for character in catalog["characters"]:
            if character["type"] == "research":
                paths = [character["profile"], character["license"]["path"]]
                if character.get("sourceTerms"):
                    paths.append(character["sourceTerms"])
            elif character["type"] == "pack":
                paths = []
                for variant in character["variants"]:
                    download = variant["download"]
                    archive = ROOT / download["path"]
                    if not archive.is_file():
                        raise RuntimeError("Download archives are missing. Run python3 scripts/fetch-downloads.py first.")
                    if archive.stat().st_size != download["bytes"] or hashlib.sha256(archive.read_bytes()).hexdigest() != download["sha256"]:
                        raise RuntimeError(f"Archive does not match catalog checksum: {archive.name}")
                    paths.extend([download["path"], variant["preview"]["idle"], *variant["preview"]["running"], variant["license"]["path"]])
                    if variant["sourceTerms"]:
                        paths.append(variant["sourceTerms"])
            else:
                raise ValueError(f"Unsupported character type: {character['type']}")
            for relative in paths:
                destination = stage / relative
                if destination.is_file():
                    continue
                source = (ROOT / relative).resolve(strict=True)
                source.relative_to(ROOT)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)
        if output.exists():
            shutil.rmtree(output)
        shutil.move(str(stage), output)
    print(f"Built {output}: {len(catalog['characters'])} characters; no authoring sources or bundled default included")


if __name__ == "__main__":
    main()

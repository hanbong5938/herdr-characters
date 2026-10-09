#!/usr/bin/env python3
"""Build optional pack archives and previews with Herdr's real native renderer."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from catalog_inventory import synchronize_catalog

ROOT = Path(__file__).resolve().parents[1]


def run(command):
    result = subprocess.run([str(value) for value in command], text=True, capture_output=True, timeout=120)
    if result.returncode:
        raise RuntimeError(f"Command failed: {' '.join(map(str, command))}\n{result.stdout}{result.stderr}")
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native", required=True, type=Path)
    parser.add_argument("--app-source", type=Path, default=os.environ.get("HERDR_DESKTOP_PET_SOURCE"))
    args = parser.parse_args()
    if args.app_source is None:
        parser.error("pass --app-source or set HERDR_DESKTOP_PET_SOURCE")
    native = args.native.resolve(strict=True)
    creator = (args.app_source / "tools/character-pack.py").resolve(strict=True)
    source = json.loads((ROOT / "catalog.source.json").read_text())
    catalog = {key: source[key] for key in ("schemaVersion", "repositoryUrl", "submissionUrl", "releaseTag")}
    catalog["characters"] = []
    with tempfile.TemporaryDirectory(prefix="herdr-catalog-") as temporary:
        stage = Path(temporary)
        (stage / "downloads").mkdir()
        (stage / "previews").mkdir()
        for character in source["characters"]:
            item = {key: character[key] for key in ("id", "name", "description", "author", "tags", "type")}
            if "displayName" in character:
                item["displayName"] = character["displayName"]
            if character["type"] == "research":
                item.update({key: character[key] for key in ("publishedAt", "profile", "sourceUrl", "license")})
                item["sourceTerms"] = character.get("sourceTerms")
                profile = (ROOT / item["profile"]).resolve(strict=True)
                shutil.copy2(profile, stage / "previews" / profile.name)
                catalog["characters"].append(item)
                continue
            if character["type"] != "pack":
                raise ValueError(f"Unsupported character type: {character['type']}")
            item["variants"] = []
            for spec in character["variants"]:
                pack = (ROOT / spec["path"]).resolve(strict=True)
                pack.relative_to(ROOT / "packs")
                manifest = json.loads((pack / "manifest.json").read_text())
                pack_id = manifest["id"]
                archive_name = f"{pack_id}-v{spec['version']}.herdrchar"
                archive = stage / "downloads" / archive_name
                run(["python3", creator, "package", "--path", pack, "--native", native, "--output", archive])
                profile = ["--config-dir", stage / "config", "--state-dir", stage / "state"]
                idle_name = f"{pack_id}-idle.png"
                run([native, "pack", "preview", "--path", pack, "--output", stage / "previews" / idle_name, "--phase", "idle", "--time-ms", "0", *profile])
                running = []
                for index, time_ms in enumerate((0, 350, 700, 1050)):
                    name = f"{pack_id}-running-{index}.png"
                    run([native, "pack", "preview", "--path", pack, "--output", stage / "previews" / name, "--phase", "running", "--time-ms", str(time_ms), *profile])
                    running.append(f"previews/{name}")
                license_path = next(entry["path"] for entry in manifest["licenses"])
                terms = next((name for name in ("SOURCE_TERMS.txt", "NOTICE.txt") if (pack / name).is_file()), None)
                license = {"label": spec["licenseLabel"], "path": f"{spec['path']}/{license_path}"}
                if "licenseDisplayLabel" in spec:
                    license["displayLabel"] = spec["licenseDisplayLabel"]
                item["variants"].append({
                    "id": pack_id,
                    "name": spec["name"],
                    "version": spec["version"],
                    "formatVersion": manifest["version"],
                    "renderMode": manifest["render_mode"],
                    "publishedAt": spec["publishedAt"],
                    "download": {
                        "path": f"downloads/{archive_name}",
                        "bytes": archive.stat().st_size,
                        "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
                    },
                    "preview": {"idle": f"previews/{idle_name}", "running": running},
                    "license": license,
                    "sourceTerms": f"{spec['path']}/{terms}" if terms else None,
                })
                print(f"Prepared {pack_id}: validated archive and five native previews")
            catalog["characters"].append(item)
        catalog = synchronize_catalog(ROOT, catalog, stage / "previews")
        checksums = "".join(f"{variant['download']['sha256']}  {Path(variant['download']['path']).name}\n" for item in catalog["characters"] if item["type"] == "pack" for variant in item["variants"])
        (stage / "downloads/SHA256SUMS").write_text(checksums)
        # Keep standalone curated profiles that are not regenerated by this build.
        existing_previews = ROOT / "previews"
        if existing_previews.is_dir():
            for profile in existing_previews.glob("*-profile.png"):
                staged_profile = stage / "previews" / profile.name
                if profile.is_file() and not staged_profile.exists():
                    shutil.copy2(profile, staged_profile)
        # Authored research profiles were staged above; discovered sources use
        # manifest entry previews produced by synchronize_catalog.
        # Publish only after every selected pack has passed native validation/rendering.
        for directory in ("downloads", "previews"):
            destination = ROOT / directory
            if destination.exists():
                shutil.rmtree(destination)
            shutil.move(str(stage / directory), destination)
        (ROOT / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    print(f"Catalog ready: {len(catalog['characters'])} characters, {sum(len(item['variants']) for item in catalog['characters'] if item['type'] == 'pack')} packs")


if __name__ == "__main__":
    main()

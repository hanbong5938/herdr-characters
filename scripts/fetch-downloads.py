#!/usr/bin/env python3
"""Fetch this catalog's pinned public GitHub release assets anonymously."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
from urllib.parse import quote, urlparse
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


def main():
    catalog = json.loads((ROOT / "catalog.json").read_text())
    repository_url = urlparse(catalog["repositoryUrl"])
    if repository_url.scheme != "https" or repository_url.netloc != "github.com":
        raise RuntimeError("repositoryUrl must name the GitHub repository that owns the pack release")
    repository = repository_url.path.strip("/")
    variants = [variant for character in catalog["characters"] if character["type"] == "pack" for variant in character["variants"]]
    release_url = f"https://github.com/{repository}/releases/download/{quote(catalog['releaseTag'], safe='')}"
    with tempfile.TemporaryDirectory(prefix="herdr-downloads-") as temporary:
        stage = Path(temporary)
        assets = [Path(variant["download"]["path"]).name for variant in variants] + ["SHA256SUMS"]
        for name in assets:
            with urlopen(f"{release_url}/{quote(name, safe='')}") as response, (stage / name).open("wb") as destination:
                shutil.copyfileobj(response, destination)
        for variant in variants:
            download = variant["download"]
            archive = stage / Path(download["path"]).name
            if archive.stat().st_size != download["bytes"] or hashlib.sha256(archive.read_bytes()).hexdigest() != download["sha256"]:
                raise RuntimeError(f"Release archive does not match the catalog: {archive.name}")
        destination = ROOT / "downloads"
        if destination.exists():
            shutil.rmtree(destination)
        shutil.move(str(stage), destination)
    print(f"Fetched and verified {len(variants)} pinned character archives")


if __name__ == "__main__":
    main()

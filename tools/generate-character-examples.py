#!/usr/bin/env python3
"""Generate the v4 Coding Cat example from the original drawing utility.

The generator uses only Python's standard library plus the repository's own
``tools/generate-character.py`` module. It never downloads or executes pack
content. Use --replace explicitly when regenerating an existing output tree.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
from typing import Any


PHASES = ("idle", "running", "waiting", "unknown")
REACTION_SOURCES = {
    "head_tap": "unknown",
    "body_tap": "running",
    "pet": "waiting",
    "completion_observed": "idle",
}
REGIONS = {
    "phase-idle.png": {"head": {"x0": 78, "y0": 42, "x1": 300, "y1": 245}, "body": {"x0": 54, "y0": 224, "x1": 330, "y1": 474}},
    "phase-running.png": {"head": {"x0": 82, "y0": 34, "x1": 306, "y1": 244}, "body": {"x0": 48, "y0": 216, "x1": 338, "y1": 474}},
    "phase-waiting.png": {"head": {"x0": 78, "y0": 42, "x1": 354, "y1": 250}, "body": {"x0": 54, "y0": 224, "x1": 330, "y1": 474}},
    "phase-unknown.png": {"head": {"x0": 78, "y0": 48, "x1": 350, "y1": 252}, "body": {"x0": 54, "y0": 230, "x1": 330, "y1": 480}},
    "reaction-head-tap.png": {"head": {"x0": 78, "y0": 48, "x1": 350, "y1": 252}, "body": {"x0": 54, "y0": 230, "x1": 330, "y1": 480}},
    "reaction-body-tap.png": {"head": {"x0": 82, "y0": 34, "x1": 306, "y1": 244}, "body": {"x0": 48, "y0": 216, "x1": 338, "y1": 474}},
    "reaction-pet.png": {"head": {"x0": 78, "y0": 42, "x1": 354, "y1": 250}, "body": {"x0": 54, "y0": 224, "x1": 330, "y1": 474}},
    "reaction-completion-observed.png": {"head": {"x0": 78, "y0": 42, "x1": 300, "y1": 245}, "body": {"x0": 54, "y0": 224, "x1": 330, "y1": 474}},
}

LICENSE = """Coding Cat example character artwork and Herdr creator example

Copyright (c) 2026 Herdr contributors
SPDX-License-Identifier: MIT

This payload covers the original Coding Cat PNG artwork copied from the
repository's deterministic drawing utility and the authored v4 clip metadata.
The utility source is tools/generate-character.py. The four phase images and
reaction images are transparent RGBA raster outputs of original hand-authored
geometry and palette in that utility. No third-party artwork, provider output,
model output, or external asset is included or asserted. No human-trial status
is claimed by this example.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
ATTRIBUTION = """Coding Cat is an original Herdr contributors character. Its transparent RGBA
frames use the repository's original coding-cat drawing utility at
tools/generate-character.py. Four phase clips and four semantic reaction clips
are authored in entry.json, with explicit head and body regions for every
unique frame. This attribution records provenance only; no human trial or
third-party authorship is claimed.
"""
SOURCE = """method: procedural
generator: tools/generate-character.py
source-root: tools/generate-character.py
artifacts: transparent RGBA PNG frames and entry.json
canvas: 384x512
clip-policy: four authored phases and four authored semantic reactions; every frame has explicit head/body regions
rights: original repository-authored artwork, MIT
provider: none
model: none
"""


def load_drawing_module(path: Path) -> Any:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"drawing utility is unavailable or is a symlink: {path}")
    spec = importlib.util.spec_from_file_location("herdr_original_character", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load drawing utility: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_text(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as destination:
        destination.write(text)


def payload_kind(name: str) -> str:
    upper = name.upper()
    if name.endswith(".png"):
        return "png"
    if name == "entry.json":
        return "entry"
    if "LICENSE" in upper:
        return "license"
    if "ATTRIBUTION" in upper:
        return "attribution"
    return "source"


def build_entry() -> dict[str, Any]:
    return {
        "version": 1,
        "phases": {
            "idle": {"fps": 4, "frames": ["phase-idle.png"]},
            "running": {"fps": 8, "frames": ["phase-running.png"]},
            "waiting": {"fps": 3, "frames": ["phase-waiting.png"]},
            "unknown": {"fps": 5, "frames": ["phase-unknown.png"]},
        },
        "reactions": {
            "head_tap": {"frames": ["reaction-head-tap.png"]},
            "body_tap": {"frames": ["reaction-body-tap.png"]},
            "pet": {"frames": ["reaction-pet.png"]},
            "completion_observed": {"frames": ["reaction-completion-observed.png"]},
        },
        "regions": REGIONS,
    }


def build_manifest(root: Path) -> dict[str, Any]:
    payloads: list[dict[str, Any]] = []
    for path in sorted(root.iterdir(), key=lambda item: item.name):
        if path.name == "manifest.json":
            continue
        data = path.read_bytes()
        payloads.append({"path": path.name, "size": len(data), "sha256": hashlib.sha256(data).hexdigest(), "kind": payload_kind(path.name)})
    return {
        "format": "herdr.character",
        "version": 4,
        "render_mode": "png",
        "id": "coding-cat",
        "name": "Coding Cat",
        "width": 384,
        "height": 512,
        "author": {"name": "Herdr contributors"},
        "source": {
            "method": "procedural",
            "description": "Original transparent Coding Cat raster artwork from the repository's deterministic drawing utility, with authored four-phase and four-reaction clips and explicit frame interaction regions.",
            "urls": ["tools/generate-character.py"],
        },
        "licenses": [{"expression": "MIT", "path": "LICENSE.txt"}],
        "attributions": ["ATTRIBUTION.txt"],
        "entry": "entry.json",
        "runtime": {"name": "herdr-native-png", "version": 1, "capabilities": ["frame-clips", "frame-regions"]},
        "payloads": payloads,
        "persona": "A bright coding cat that keeps an eye on the work and celebrates small wins.",
        "dialogue": {
            "en": {
                "phases": {
                    "idle": "I'm ready.",
                    "running": "I'm working through it.",
                    "waiting": "I'm waiting for the next step.",
                    "unknown": "I'm checking the signal.",
                },
                "reactions": {
                    "head_tap": "Hello there!",
                    "body_tap": "Let's keep going.",
                    "pet": "That feels nice.",
                    "completion_observed": "We did it!",
                },
            }
        },
    }


def prepare_output(path: Path, replace: bool) -> None:
    if path.exists() or path.is_symlink():
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise RuntimeError(f"output must be a real directory: {path}")
        if not replace:
            raise RuntimeError(f"output already exists; pass --replace explicitly: {path}")
        allowed = set(REGIONS) | {"manifest.json", "entry.json", "LICENSE.txt", "ATTRIBUTION.txt", "SOURCE.txt"}
        entries = list(path.iterdir())
        if entries:
            manifest = path / "manifest.json"
            if not manifest.is_file() or manifest.is_symlink():
                raise RuntimeError(f"refusing to replace a directory without a generated manifest: {path}")
            identity = json.loads(manifest.read_text(encoding="utf-8"))
            if identity.get("format") != "herdr.character" or identity.get("id") != "coding-cat":
                raise RuntimeError(f"refusing to replace a different character or directory: {path}")
        if any(entry.name not in allowed or entry.is_symlink() or not entry.is_file() for entry in entries):
            raise RuntimeError(f"refusing to delete unrelated files or directories: {path}")
        for entry in entries:
            entry.unlink()
        path.rmdir()
    path.mkdir(parents=True, mode=0o700)


def reaction_image(module: Any, reaction: str, source_phase: str) -> bytes:
    """Add a small authored semantic accent to an existing original pose."""
    canvas = module.draw_character(source_phase)
    if reaction == "head_tap":
        canvas.stroke(((112, 56), (99, 45)), module.GOLD, 5)
        canvas.stroke(((272, 56), (285, 45)), module.GOLD, 5)
        canvas.stroke(((107, 74), (91, 74)), module.PINK, 4)
        canvas.stroke(((277, 74), (293, 74)), module.PINK, 4)
    elif reaction == "body_tap":
        canvas.stroke(((92, 325), (72, 338), (92, 351)), module.TEAL, 5)
        canvas.stroke(((292, 325), (312, 338), (292, 351)), module.TEAL, 5)
    elif reaction == "pet":
        for left in (48, 318):
            canvas.ellipse((left, 102, left + 10, 113), module.PINK_LIGHT)
            canvas.ellipse((left + 8, 102, left + 18, 113), module.PINK_LIGHT)
            canvas.polygon(((left, 108), (left + 18, 108), (left + 9, 125)), module.PINK_LIGHT)
    elif reaction == "completion_observed":
        canvas.stroke(((64, 66), (64, 94)), module.GOLD, 4)
        canvas.stroke(((50, 80), (78, 80)), module.GOLD, 4)
        canvas.stroke(((320, 66), (320, 94)), module.GOLD, 4)
        canvas.stroke(((306, 80), (334, 80)), module.GOLD, 4)
    else:
        raise ValueError(f"unsupported reaction {reaction!r}")
    return canvas.downsample()


def generate(output: Path, utility: Path, replace: bool) -> None:
    module = load_drawing_module(utility)
    prepare_output(output, replace)
    try:
        write_text(output / "LICENSE.txt", LICENSE)
        write_text(output / "ATTRIBUTION.txt", ATTRIBUTION)
        write_text(output / "SOURCE.txt", SOURCE)
        for phase in PHASES:
            image = module.draw_character(phase).downsample()
            module.write_png(output / f"phase-{phase}.png", image)
        for reaction, source_phase in REACTION_SOURCES.items():
            image = reaction_image(module, reaction, source_phase)
            module.write_png(output / f"reaction-{reaction.replace('_', '-')}.png", image)
        write_text(output / "entry.json", json.dumps(build_entry(), ensure_ascii=False, indent=2, separators=(",", ": ")) + "\n")
        write_text(output / "manifest.json", json.dumps(build_manifest(output), ensure_ascii=False, indent=2, separators=(",", ": ")) + "\n")
    except Exception:
        shutil.rmtree(output, ignore_errors=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parents[1]
    parser.add_argument("--output", type=Path, default=default_root / "packs" / "png-example")
    parser.add_argument("--generator", type=Path, default=Path(__file__).resolve().with_name("generate-character.py"))
    parser.add_argument("--replace", action="store_true", help="replace an existing output directory")
    args = parser.parse_args()
    try:
        generate(args.output.resolve(), args.generator.resolve(), args.replace)
    except (OSError, RuntimeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

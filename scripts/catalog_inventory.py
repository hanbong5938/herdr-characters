"""Complete a gallery catalog from pack manifests without publishing source-only archives."""

import json
from pathlib import Path


def _object(value, path):
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def _text(value, path):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path}: expected nonempty text")
    return value


def _read_json(path):
    try:
        return _object(json.loads(path.read_text(encoding="utf-8")), path)
    except (OSError, ValueError) as error:
        raise ValueError(f"{path}: invalid or missing JSON: {error}") from error


def _within(root, relative, context):
    name = _text(relative, context)
    path = Path(name)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{context}: unsafe path {name!r}")
    try:
        base = root.resolve(strict=True)
        target = (base / path).resolve(strict=True)
        target.relative_to(base)
    except (OSError, ValueError) as error:
        raise ValueError(f"{context}: missing or out-of-pack file {name!r}") from error
    if not target.is_file():
        raise ValueError(f"{context}: not a file: {name!r}")
    return target


def _preview_source(pack, manifest, manifest_path):
    renderer = manifest.get("render_mode")
    if renderer not in ("png", "rig"):
        raise ValueError(f"{manifest_path}: unsupported renderer {renderer!r}")
    entry_path = _within(pack, manifest.get("entry"), f"{manifest_path}: entry")
    entry = _read_json(entry_path)
    if renderer == "png":
        try:
            source = entry["phases"]["idle"]["frames"][0]
        except (KeyError, IndexError, TypeError) as error:
            raise ValueError(f"{entry_path}: missing declared idle frame") from error
        suffix = ".png"
    else:
        try:
            initial = entry["initial"]
            source = next(model["file"] for model in entry["models"] if model["id"] == initial)
        except (KeyError, StopIteration, TypeError) as error:
            raise ValueError(f"{entry_path}: missing initial model file") from error
        suffix = ".psd"
    path = _within(pack, source, f"{entry_path}: preview source")
    if path.suffix.lower() != suffix:
        raise ValueError(f"{entry_path}: expected {suffix} preview source, got {path}")
    return path


def _source_preview(source, destination):
    from PIL import Image

    try:
        with Image.open(source) as original:
            image = original.convert("RGBA")
        image.thumbnail((512, 512), Image.Resampling.LANCZOS)
        destination.parent.mkdir(parents=True, exist_ok=True)
        image.save(destination, format="PNG")
    except (OSError, ValueError) as error:
        raise ValueError(f"{source}: cannot decode preview image: {error}") from error


def _approval_date(pack):
    approval_path = pack / "owner-approval.json"
    if not approval_path.is_file():
        return None
    approval = _read_json(approval_path).get("wardrobeRepositorySourceApproval", {})
    if isinstance(approval, dict) and (approval.get("approved") is True or approval.get("publicRepositorySourceInclusionApproved") is True):
        return _text(approval.get("date"), f"{approval_path}: wardrobeRepositorySourceApproval.date")
    return None


def synchronize_catalog(root: Path, catalog: dict, preview_directory: Path) -> dict:
    """Return all discovered packs; write only derived source previews into preview_directory.

    Published archive metadata comes from catalog. Authored research profiles in
    catalog.source.json override generated research records; every other source-only
    record is freshly derived from its manifest on each call.
    """
    root = root.resolve()
    catalog = _object(catalog, "catalog")
    if catalog.get("schemaVersion") != 1:
        raise ValueError("catalog: unsupported schemaVersion (expected 1)")
    entries = catalog.get("characters")
    if not isinstance(entries, list):
        raise ValueError("catalog: characters must be a list")
    source_path = root / "catalog.source.json"
    source = _read_json(source_path) if source_path.is_file() else {"characters": []}
    overrides = source.get("characters", [])
    if not isinstance(overrides, list):
        raise ValueError(f"{source_path}: characters must be a list")
    authored = {}
    for index, item in enumerate(overrides):
        item = _object(item, f"{source_path}: characters[{index}]")
        identifier = _text(item.get("id"), f"{source_path}: characters[{index}].id")
        if identifier in authored:
            raise ValueError(f"{source_path}: duplicate id {identifier!r}")
        authored[identifier] = item
    published = {}
    seen_catalog_ids = set()
    for index, item in enumerate(entries):
        item = _object(item, f"catalog: characters[{index}]")
        identifier = _text(item.get("id"), f"catalog: characters[{index}].id")
        if identifier in seen_catalog_ids:
            raise ValueError(f"catalog: duplicate id {identifier!r}")
        seen_catalog_ids.add(identifier)
        if item.get("type") == "pack":
            published[identifier] = item
        elif item.get("type") != "research":
            raise ValueError(f"catalog: characters[{index}]: unsupported type {item.get('type')!r}")
    packs = root / "packs"
    if not packs.is_dir():
        raise ValueError(f"{packs}: missing packs directory")
    discovered = {}
    for directory in sorted(packs.iterdir()):
        if not directory.is_dir():
            continue
        manifest_path = directory / "manifest.json"
        if not manifest_path.is_file():
            raise ValueError(f"{manifest_path}: missing pack manifest")
        manifest = _read_json(manifest_path)
        if manifest.get("format") != "herdr.character" or not isinstance(manifest.get("version"), int):
            raise ValueError(f"{manifest_path}: invalid character format/version")
        identifier = _text(manifest.get("id"), f"{manifest_path}: id")
        if not all(ch.isascii() and (ch.islower() or ch.isdigit() or ch == "-") for ch in identifier) or identifier.startswith("-") or identifier.endswith("-"):
            raise ValueError(f"{manifest_path}: invalid id {identifier!r}")
        if identifier in discovered:
            raise ValueError(f"{manifest_path}: duplicate id {identifier!r} (also {discovered[identifier][1]})")
        _text(manifest.get("name"), f"{manifest_path}: name")
        _text(_object(manifest.get("author"), f"{manifest_path}: author").get("name"), f"{manifest_path}: author.name")
        licenses = manifest.get("licenses")
        if not isinstance(licenses, list) or not licenses:
            raise ValueError(f"{manifest_path}: missing licenses")
        for index, license_entry in enumerate(licenses):
            license_entry = _object(license_entry, f"{manifest_path}: licenses[{index}]")
            _text(license_entry.get("expression"), f"{manifest_path}: licenses[{index}].expression")
            _within(directory, license_entry.get("path"), f"{manifest_path}: licenses[{index}].path")
        preview_source = _preview_source(directory, manifest, manifest_path)
        discovered[identifier] = (directory, manifest_path, manifest, preview_source)

    represented = set()
    for identifier, item in published.items():
        variants = item.get("variants")
        if not isinstance(variants, list) or not variants:
            raise ValueError(f"catalog: published pack {identifier!r} has no variants")
        for index, variant in enumerate(variants):
            variant = _object(variant, f"catalog: published pack {identifier!r} variants[{index}]")
            variant_id = _text(variant.get("id"), f"catalog: published pack {identifier!r} variants[{index}].id")
            if variant_id not in discovered:
                raise ValueError(f"catalog: published pack {identifier!r} variant {variant_id!r} has no manifest")
            if variant_id in represented:
                raise ValueError(f"catalog: manifest {variant_id!r} is represented by multiple published variants")
            represented.add(variant_id)
    for identifier, item in authored.items():
        if identifier in published:
            if item.get("type") != "pack":
                raise ValueError(f"{source_path}: published group {identifier!r} must be a pack")
        elif item.get("type") == "pack":
            raise ValueError(f"{source_path}: published pack {identifier!r} lacks built archive metadata")
        elif identifier not in discovered:
            raise ValueError(f"{source_path}: authored character {identifier!r} has no manifest")
        elif identifier in represented:
            raise ValueError(f"{source_path}: authored character {identifier!r} duplicates a published variant")
    for identifier in published:
        if identifier in discovered and identifier not in represented:
            raise ValueError(f"catalog: published group {identifier!r} conflicts with unrepresented manifest")

    result = {key: value for key, value in catalog.items() if key != "characters"}
    result["characters"] = []
    for identifier in [*sorted(published), *(key for key in sorted(authored) if key not in published),
                       *(key for key in sorted(discovered) if key not in represented and key not in authored
                         and key not in published)]:
        if identifier in published:
            result["characters"].append(published[identifier])
            continue
        pack, manifest_path, manifest, preview_source = discovered[identifier]
        authored_item = authored.get(identifier)
        if authored_item is not None and authored_item.get("type") != "research":
            raise ValueError(f"{source_path}: unsupported character type for {identifier!r}")
        if authored_item is not None:
            profile = _within(root, authored_item.get("profile"), f"{source_path}: {identifier}.profile")
            try:
                profile.relative_to((root / "previews").resolve(strict=True))
            except ValueError as error:
                raise ValueError(f"{source_path}: {identifier}.profile must be inside previews") from error
            item = dict(authored_item)
            item["type"] = "research"
        else:
            profile_path = f"previews/{identifier}-source.png"
            _source_preview(preview_source, preview_directory / f"{identifier}-source.png")
            name = manifest["name"]
            terms = next((filename for filename in ("SOURCE_TERMS.txt", "NOTICE.txt") if (pack / filename).is_file()), None)
            if terms:
                _within(pack, terms, f"{manifest_path}: sourceTerms")
            license_entry = manifest["licenses"][0]
            item = {
                "id": identifier,
                "type": "research",
                "name": name,
                "description": {
                    "en": f"Source files and artwork preview for {name}; no downloadable gallery pack is offered here.",
                    "ko": f"{name} 소스 파일과 아트워크 미리보기입니다. 이 갤러리에서 다운로드 가능한 팩은 제공하지 않습니다.",
                },
                "author": manifest["author"]["name"],
                "tags": list(dict.fromkeys([identifier, *identifier.split("-"), name, "source", "research", "소스", "연구"])),
                "publishedAt": _approval_date(pack),
                "profile": profile_path,
                "sourceUrl": f"{_text(catalog.get('repositoryUrl'), 'catalog.repositoryUrl').rstrip('/')}/tree/main/packs/{pack.name}",
                "license": {"label": license_entry["expression"], "path": f"packs/{pack.name}/{license_entry['path']}"},
                "sourceTerms": f"packs/{pack.name}/{terms}" if terms else None,
            }
        for relative, label in ((item["license"]["path"], "catalog license"), (item.get("sourceTerms"), "sourceTerms")):
            if relative:
                path = _within(root, relative, f"{manifest_path}: {label}")
                try:
                    path.relative_to(pack.resolve(strict=True))
                except ValueError as error:
                    raise ValueError(f"{manifest_path}: {label} must be inside {pack}") from error
        result["characters"].append(item)
    return result

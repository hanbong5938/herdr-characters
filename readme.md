# Herdr characters

[한국어](readme.ko.md)

This public character library offers **Coding Cat as its only downloadable pack**, alongside Arin's owner-approved public profile preview and [research source files](packs/arin-research), but no Arin packaged release. Coding Cat is an original, MIT-licensed procedural PNG character pack for Herdr Desktop Pet. Coding Cat uses character format v4, transparent 384×512 PNG frames, four phase clips (idle, running, waiting, unknown), and four reaction clips (head tap, body tap, pet, completion observed). The pack and its source notices are in [`packs/png-example`](packs/png-example); the deterministic drawing utility is [`tools/generate-character.py`](tools/generate-character.py). The repository-level [MIT license](LICENSE.txt) covers the original source utilities and fixture.

## Character previews

<table>
  <tr>
    <td align="center" width="180"><a href="previews/coding-cat-profile.png"><img src="previews/coding-cat-profile.png" alt="Coding Cat profile preview" width="160"></a><br><strong>Coding Cat</strong><br>Optional download<br>MIT</td>
    <td align="center" width="180"><a href="previews/arin-research-profile.png"><img src="previews/arin-research-profile.png" alt="Arin research profile preview" width="160"></a><br><strong>Arin</strong><br>Profile preview<br>No pack release</td>
  </tr>
</table>

Coding Cat is the optional downloadable [MIT-licensed pack](packs/png-example/SOURCE.txt). Arin's [owner approval](packs/arin-research/owner-approval.json) covers public profile display and publication of [repository research sources](packs/arin-research), including PSDs; no official Arin archive, catalog download or installable release is available. Arin artwork remains subject to its separate [research-use terms](packs/arin-research/LICENSE.txt).

## Rubelia wardrobe sources

The canonical school-uniform and swimsuit source packs moved from the private archive into this shared repository. Artwork, ten-pose PSDs, rigs and motion are unchanged; only names and repository-source approval metadata were updated.

| Korean pack name | English display | Canonical source |
| --- | --- | --- |
| 루벨리아(교복) | Rubelia (School Uniform) | [`packs/rubelia-school-uniform`](packs/rubelia-school-uniform) |
| 루벨리아(수영복) | Rubelia (Swimsuit) | [`packs/rubelia-white-bikini`](packs/rubelia-white-bikini) |

The user selected inclusion of both packs as public repository sources. Each `owner-approval.json` records that user assertion, not independently verified clearance or a new model license. Source and Qwen terms remain in each pack's `NOTICE.txt`, `LICENSE.txt` and `QWEN_RESEARCH_LICENSE.txt`. This migration performed no commit, push or official packaged release and did not add the packs to the public download catalog.

The private local gallery references these same canonical sources and uses the Korean/English display names above. Installed manifest names remain single Korean strings; automatic name switching with the app language is not supported.


## Download and import

Download [`coding-cat-v0.0.2.herdrchar`](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.2/coding-cat-v0.0.2.herdrchar) and [`SHA256SUMS`](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.2/SHA256SUMS) from the public `packs-v0.0.2` release. Verify the downloaded archive against `SHA256SUMS` with `shasum -a 256 -c SHA256SUMS` from the download directory; the generated [`catalog.json`](catalog.json) also records the archive's exact byte count and SHA-256 digest. Do not substitute a hash from this page.

Import the archive with the Herdr Desktop Pet native executable, then **select it separately**; importing alone does not make it active:

```sh
PET="/path/to/herdr-desktop-pet"
"$PET" pack import --path "/absolute/path/to/coding-cat-v0.0.2.herdrchar"
"$PET" pack select coding-cat
```

Replace `PET` and the archive path with actual local paths. Alternatively, use the app's Characters tab to import the archive, choose Coding Cat, then click **Apply**.

## Recreate the source fixture

The two original utilities use the Python standard library and require no asset service or third-party artwork. Run from this repository's root:

```sh
python3 tools/generate-character.py --output sources/legacy-png
python3 tools/generate-character-examples.py --output packs/png-example --replace
```

The first command recreates the original legacy four-pose raster fixture; the second recreates the v4 Coding Cat example pack from the drawing utility. `--replace` is required when `packs/png-example` already exists; do not use it on a pack with local modifications you want to keep.

## Build the catalog and gallery

To package and validate the example and render gallery previews, supply the Herdr native executable and a local Herdr Desktop Pet source checkout containing `tools/character-pack.py`:

```sh
python3 scripts/build-catalog.py --native /absolute/path/to/herdr-desktop-pet --app-source /absolute/path/to/herdr-pet
python3 scripts/build-gallery.py
```

`build-catalog.py` reads [`catalog.source.json`](catalog.source.json), generates `catalog.json`, `downloads/coding-cat-v0.0.2.herdrchar`, `downloads/SHA256SUMS`, and five native preview images; `build-gallery.py` stages the static site in `dist/gallery` and checks the archive against the generated catalog. To retrieve the **already published** release assets anonymously instead of locally packaging them, first obtain the matching generated `catalog.json`, then run `python3 scripts/fetch-downloads.py` before `python3 scripts/build-gallery.py`. The fetch script rejects archives whose byte length or SHA-256 differs from the catalog. Gallery preview images must already exist locally when building a gallery from fetched archives.

Standalone repository profile images include [`previews/coding-cat-profile.png`](previews/coding-cat-profile.png), made from Coding Cat's existing default idle image, and [`previews/arin-research-profile.png`](previews/arin-research-profile.png), cropped from Arin's native waiting render (see [`packs/arin-research/source-record.json`](packs/arin-research/source-record.json)). The owner's dated, asserted public README profile-display and repository-source publication approvals are recorded in [`packs/arin-research/owner-approval.json`](packs/arin-research/owner-approval.json); they are not independently verified legal clearance and do not authorize an official packaged release, commercial use, model-material rights, or app catalog/menu availability. Catalog regeneration preserves these profile PNGs without adding them to the catalog or generated gallery.

Coding Cat profile provenance: source [`previews/coding-cat-idle.png`](previews/coding-cat-idle.png), SHA-256 `35df3d4346005167b645e0997723ad2e59404729fc895518733fe83629aa286d` (384×512 RGBA); face-centered square crop `[84, 35, 300, 251]` in source pixels (left, top, right, bottom), resized with LANCZOS to 512×512 RGBA PNG. Output [`previews/coding-cat-profile.png`](previews/coding-cat-profile.png) has SHA-256 `aa75304d0c0e7d570dc39465ccec8fc7af369efbbff970119e15f228a900ea3a`. Source transparency is retained; no AI generation, retouching, or new background. Rights remain unchanged: original repository-authored artwork, MIT, as recorded in [`packs/png-example/SOURCE.txt`](packs/png-example/SOURCE.txt).

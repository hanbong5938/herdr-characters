# Herdr characters

[한국어](readme.ko.md)

This public character library lists all four current pack records: **Coding Cat is the only downloadable gallery pack**; Arin, Rubelia (School Uniform), and Rubelia (Swimsuit) are searchable source/research-only entries without gallery downloads. Coding Cat is an original, MIT-licensed procedural PNG character pack for Herdr Desktop Pet. Coding Cat uses character format v4, transparent 384×512 PNG frames, four phase clips (idle, running, waiting, unknown), and four reaction clips (head tap, body tap, pet, completion observed). The pack and its source notices are in [`packs/png-example`](packs/png-example); the deterministic drawing utility is [`tools/generate-character.py`](tools/generate-character.py). The repository-level [MIT license](LICENSE.txt) covers the original source utilities and example pack, not the separately licensed research artwork.

## Character previews

<table>
  <tr>
    <td align="center" width="180"><a href="previews/coding-cat-profile.png"><img src="previews/coding-cat-profile.png" alt="Coding Cat profile preview" width="160"></a><br><strong>Coding Cat</strong><br>Optional download<br>MIT</td>
    <td align="center" width="180"><a href="previews/arin-research-profile.png"><img src="previews/arin-research-profile.png" alt="Arin research profile preview" width="160"></a><br><strong>Arin</strong><br>Web gallery research profile<br>No pack release</td>
    <td align="center" width="180"><a href="packs/rubelia-school-uniform">Rubelia (School Uniform)</a><br>Gallery source-only preview<br>No gallery download</td>
    <td align="center" width="180"><a href="packs/rubelia-white-bikini">Rubelia (Swimsuit)</a><br>Gallery source-only preview<br>No gallery download</td>
  </tr>
</table>

Coding Cat is the optional downloadable [MIT-licensed pack](packs/png-example/SOURCE.txt). Arin is searchable as “Arin” or “아린” in the web gallery and has a profile and [repository research sources](packs/arin-research), including PSDs; no official Arin archive, catalog download or installable release is available. Arin artwork remains subject to its separate [research-use terms](packs/arin-research/LICENSE.txt). The recorded [owner approval](packs/arin-research/owner-approval.json) concerns public README profile display and repository-source publication; the current request to register a gallery research entry is distinct from that approval and does not expand rights.

## Browse the web gallery

The [gallery source](index.html) builds its catalog and aligned hero cards from every `packs/*/manifest.json`: currently Coding Cat, Arin, Rubelia (School Uniform), and Rubelia (Swimsuit). A new source pack appears on the next build or `main` push without manual registration in [`catalog.source.json`](catalog.source.json); that file supplies authored profile/publication overrides and the existing pinned Coding Cat release metadata, not the pack inventory. The original four-pose [`sources/legacy-png`](sources/legacy-png) fixture is source material for Coding Cat, not another character or installable pack. Search matches names (including Korean names), tags, descriptions and pack variant names; combine it with All, Rig, PNG or Research filters. PNG shows Coding Cat; Research shows Arin and both Rubelia source entries. Sort by publication date where recorded (unknown dates remain unknown) or by original character name using the selected language's collation. Research/source-only cards link to repository sources and terms, not gallery downloads; the Rig filter does not imply these sources are downloadable packs.

For a local preview from this repository root, install the gallery image dependency, fetch the already published Coding Cat archive, build the manifest-derived static site and serve it:

```sh
python3 -m pip install -r requirements-gallery.txt
python3 scripts/fetch-downloads.py
python3 scripts/build-gallery.py
npm run preview
```

Open `http://127.0.0.1:4187/`. Fetch uses the Python standard library and verifies only the pinned published Coding Cat archive against `catalog.json`; the gallery build uses Pillow to make source previews and writes `dist/gallery`. Neither command needs a native executable. The separate native authoring commands below regenerate the catalog, package and previews; Pages CI does **not** run them. The gallery supports narrow mobile screens and retains the current error and Retry message when switching languages after a catalog load failure.

## Publish with GitHub Pages

The public gallery is available at **[https://hanbong5938.github.io/herdr-characters/](https://hanbong5938.github.io/herdr-characters/)**. GitHub Pages uses **Settings → Pages → Build and deployment → Source: GitHub Actions** and the `github-pages` environment for `main`. A push to `main` or a manual **Actions → Deploy gallery to GitHub Pages → Run workflow** installs the pinned gallery dependency, fetches and verifies the published Coding Cat archive, discovers all current pack manifests, builds `dist/gallery`, and deploys only that static directory. Source-only previews and repository links do not publish installable archives or change source permissions. Check the workflow's `page_url` for the deployment address.

## Rubelia wardrobe sources

The canonical school-uniform and swimsuit source packs moved from the private archive into this shared repository. Artwork, ten-pose PSDs, rigs and motion are unchanged; only names and repository-source approval metadata were updated.

| Korean pack name | English display | Canonical source |
| --- | --- | --- |
| 루벨리아(교복) | Rubelia (School Uniform) | [`packs/rubelia-school-uniform`](packs/rubelia-school-uniform) |
| 루벨리아(수영복) | Rubelia (Swimsuit) | [`packs/rubelia-white-bikini`](packs/rubelia-white-bikini) |

The user selected inclusion of both packs as public repository sources. Each `owner-approval.json` records that user assertion, not independently verified clearance or a new model license. Source and Qwen terms remain in each pack's `NOTICE.txt`, `LICENSE.txt` and `QWEN_RESEARCH_LICENSE.txt`. The earlier migration performed no commit, push or official packaged release and did not add Rubelia downloads; the current gallery lists both as source-only entries, not downloadable gallery packs.

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

To package and validate the Coding Cat example and render its native gallery previews, supply the Herdr native executable and a local Herdr Desktop Pet source checkout containing `tools/character-pack.py`. Install Pillow for the source preview generation:

```sh
python3 -m pip install -r requirements-gallery.txt
python3 scripts/build-catalog.py --native /absolute/path/to/herdr-desktop-pet --app-source /absolute/path/to/herdr-pet
python3 scripts/build-gallery.py
```

Both builders discover `packs/*/manifest.json` and regenerate source-only catalog entries and previews automatically; [`catalog.source.json`](catalog.source.json) holds authored/publication overrides and pinned release data rather than a mandatory list of source packs. `build-catalog.py` regenerates `catalog.json`, the Coding Cat archive and checksums, and native Coding Cat previews. `build-gallery.py` regenerates the staged catalog in `dist/gallery`, including all four current records; only Coding Cat has a pinned gallery download and is fetched by `python3 scripts/fetch-downloads.py`. Source-only records have no variants or gallery download. Their transparent previews use the declared PNG idle image or Pillow's merged PSD composite from the authored source, not a native animation render or compatibility proof. No automatic installable Rubelia or Arin release is created.

Standalone repository profile images include [`previews/coding-cat-profile.png`](previews/coding-cat-profile.png), made from Coding Cat's existing default idle image, and [`previews/arin-research-profile.png`](previews/arin-research-profile.png), cropped from Arin's native waiting render (see [`packs/arin-research/source-record.json`](packs/arin-research/source-record.json)). The owner's dated, asserted public README profile-display and repository-source publication approvals are recorded in [`packs/arin-research/owner-approval.json`](packs/arin-research/owner-approval.json); they are not independently verified legal clearance and do not authorize an official packaged release, commercial use, model-material rights, or native app-catalog/Characters-menu registration. The current requested web-gallery research registration does not add native app-menu listing or installation support. Catalog regeneration preserves these profile PNGs and keeps Arin's research entry in the generated catalog and gallery.

Coding Cat profile provenance: source [`previews/coding-cat-idle.png`](previews/coding-cat-idle.png), SHA-256 `35df3d4346005167b645e0997723ad2e59404729fc895518733fe83629aa286d` (384×512 RGBA); face-centered square crop `[84, 35, 300, 251]` in source pixels (left, top, right, bottom), resized with LANCZOS to 512×512 RGBA PNG. Output [`previews/coding-cat-profile.png`](previews/coding-cat-profile.png) has SHA-256 `aa75304d0c0e7d570dc39465ccec8fc7af369efbbff970119e15f228a900ea3a`. Source transparency is retained; no AI generation, retouching, or new background. Rights remain unchanged: original repository-authored artwork, MIT, as recorded in [`packs/png-example/SOURCE.txt`](packs/png-example/SOURCE.txt).

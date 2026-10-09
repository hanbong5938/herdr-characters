# Herdr characters

[한국어](readme.ko.md)

The **native-validated `packs-v0.0.6` catalog** adds **Chaerin (채린) 0.0.6** as a sixth downloadable pack alongside Coding Cat, Arin, and three Rubelia variants. The five existing archive versions and bytes remain unchanged. Chaerin requires **Herdr Desktop Pet v0.3.4 or newer** for side-owned eye clipping; the other five keep their existing **v0.2.1 minimum**. Coding Cat is an original MIT-licensed procedural PNG pack (v4); the other five are independent ten-pose rig packs (v5) with separately recorded artwork terms. The repository [MIT license](LICENSE.txt) does not relicense their artwork. Confirm publication and download availability in the non-draft release; source metadata alone is not public-upload evidence.

## Character previews

<table>
  <tr>
    <td align="center" width="180"><a href="previews/coding-cat-profile.png"><img src="previews/coding-cat-profile.png" alt="Coding Cat profile preview" width="160"></a><br><strong>Coding Cat</strong><br>Optional download<br>MIT</td>
    <td align="center" width="180"><a href="previews/arin-research-profile.png"><img src="previews/arin-research-profile.png" alt="Arin profile preview" width="160"></a><br><strong>Arin</strong><br>Downloadable rig pack<br>Separate artwork terms</td>
    <td align="center" width="180"><a href="previews/chaerin-research-profile.png"><img src="previews/chaerin-research-profile.png" alt="Chaerin native profile preview" width="160"></a><br><strong>Chaerin (채린)</strong><br>0.0.6 · app v0.3.4+<br>Separate artwork/model terms</td>
    <td align="center" width="180"><a href="previews/rubelia-school-uniform-idle.png"><img src="previews/rubelia-school-uniform-idle.png" alt="Rubelia School Uniform preview" width="160"></a><br><strong>Rubelia (School Uniform)</strong><br>Downloadable rig pack</td>
    <td align="center" width="180"><a href="previews/rubelia-white-bikini-idle.png"><img src="previews/rubelia-white-bikini-idle.png" alt="Rubelia Swimsuit preview" width="160"></a><br><strong>Rubelia (Swimsuit)</strong><br>Downloadable rig pack</td>
    <td align="center" width="180"><a href="previews/rubelia-burgundy-uniform-idle.png"><img src="previews/rubelia-burgundy-uniform-idle.png" alt="Rubelia Burgundy Uniform preview" width="160"></a><br><strong>Rubelia (Burgundy Uniform)</strong><br>B short pleated skirt · 0.0.5</td>
  </tr>
</table>

Arin, Chaerin and the Rubelia wardrobe packs retain original-source hashes and owner records, including provenance linked to [`shared-world-canon`](https://github.com/hanbong5938/shared-world-canon). Chaerin's separate 2026-10-09 assertion and express approval for the downloadable/installable pack, ten PSD sources and gallery are recorded in [`owner-approval.json`](packs/chaerin-research/owner-approval.json); private editing approval alone did not cover these uses. Neither approval independently clears legal/model-material rights nor grants downstream commercial use or sublicensing. The original Chaerin registry remains commercial-blocked. Keep each pack's license, attribution and source notices with the archive.

## Browse the web gallery

The [gallery](https://hanbong5938.github.io/herdr-characters/) discovers every `packs/*/manifest.json`; [`catalog.source.json`](catalog.source.json) supplies authored profiles and explicit publication metadata. The native-validated catalog has six downloadable entries: **Rig** shows Chaerin, Arin and three Rubelia packs; **PNG** shows Coding Cat. **Research** is reserved for source-only entries and currently has none. Optional `displayName` and license `displayLabel` metadata localize gallery names and license summaries using the current language, then English, then the canonical scalar name or label. Search matches canonical and both English/Korean display names regardless of the selected language, plus tags, descriptions and variant names; alphabetic order and publication-date tie-breaking use the currently displayed names. The published [`catalog.json`](catalog.json) is regenerated from `catalog.source.json` only after successful native packaging; source-only changes are not a live gallery update.

For a local preview, install the gallery image dependency, fetch all six pinned release archives, build the static site and serve it:

```sh
python3 -m pip install -r requirements-gallery.txt
python3 scripts/fetch-downloads.py
python3 scripts/build-gallery.py
npm run preview
```

Open `http://127.0.0.1:4187/`. Fetch uses the Python standard library and checks every pinned archive's bytes and SHA-256 against `catalog.json`; the gallery build writes `dist/gallery`. Neither command needs the native app. Native authoring commands below regenerate the archives and animated previews; Pages CI only fetches the already published release. The gallery supports narrow mobile screens and retains its error/Retry state when switching languages after a catalog load failure.

## Publish with GitHub Pages

The public gallery is **[https://hanbong5938.github.io/herdr-characters/](https://hanbong5938.github.io/herdr-characters/)**. GitHub Pages uses **GitHub Actions** and the `github-pages` environment. Publish all six target release assets **before pushing the regenerated catalog to `main`**: the Pages workflow fetches and verifies every pinned archive, builds `dist/gallery`, and deploys that directory. A source-only preview or repository link does not authorize an installable release.

## Rubelia wardrobe sources

The school-uniform and swimsuit sources moved from the private archive into this shared repository. Original artwork, ten-pose PSDs, rigs and motion are unchanged; publication approval and license/provenance notices now record the owner-approved `packs-v0.0.3` downloads.

| Korean pack name | English display | Canonical source |
| --- | --- | --- |
| 루벨리아(교복) | Rubelia (School Uniform) | [`packs/rubelia-school-uniform`](packs/rubelia-school-uniform) |
| 루벨리아(수영복) | Rubelia (Swimsuit) | [`packs/rubelia-white-bikini`](packs/rubelia-white-bikini) |
| 루벨리아(제복) | Rubelia (Burgundy Uniform) | [`packs/rubelia-burgundy-uniform`](packs/rubelia-burgundy-uniform) |

The earlier source-only migration did not publish installable archives. The user subsequently approved publishing all four packs as downloads; both Rubelia `owner-approval.json` files record this separate authorization. Their `NOTICE.txt`, `LICENSE.txt` and `QWEN_RESEARCH_LICENSE.txt` preserve source and model provenance without granting a new downstream commercial license.

The gallery uses these same canonical sources and its localized display names are distinct from installed manifest names. Installed manifest names remain single Korean strings; automatic name switching with the app language is not supported.

## Download and import

Download the six archives and [`SHA256SUMS`](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.6/SHA256SUMS) from the non-draft [`packs-v0.0.6` release](https://github.com/hanbong5938/herdr-characters/releases/tag/packs-v0.0.6). Chaerin is the only new archive; the five prior archive versions and bytes remain unchanged. Historical `packs-v0.0.5` and earlier releases are unaffected.

| Character | Archive | Selection ID |
| --- | --- | --- |
| Coding Cat | [coding-cat-v0.0.3.herdrchar](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.6/coding-cat-v0.0.3.herdrchar) | `coding-cat` |
| Arin | [arin-research-v0.0.4.herdrchar](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.6/arin-research-v0.0.4.herdrchar) | `arin-research` |
| Chaerin (app v0.3.4+) | [chaerin-research-v0.0.6.herdrchar](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.6/chaerin-research-v0.0.6.herdrchar) | `chaerin-research` |
| Rubelia (School Uniform) | [rubelia-school-uniform-v0.0.3.herdrchar](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.6/rubelia-school-uniform-v0.0.3.herdrchar) | `rubelia-school-uniform` |
| Rubelia (Swimsuit) | [rubelia-white-bikini-v0.0.3.herdrchar](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.6/rubelia-white-bikini-v0.0.3.herdrchar) | `rubelia-white-bikini` |
| Rubelia (Burgundy Uniform) | [rubelia-burgundy-uniform-v0.0.5.herdrchar](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.6/rubelia-burgundy-uniform-v0.0.5.herdrchar) | `rubelia-burgundy-uniform` |

Download all six files alongside `SHA256SUMS`, then run `shasum -a 256 -c SHA256SUMS`. The regenerated [`catalog.json`](catalog.json) records every actual archive byte count and SHA-256.

Use the [v0.3.4 app release](https://github.com/hanbong5938/herdr-desktop-pet/releases/tag/v0.3.4) or newer for Chaerin, or v0.2.1 or newer for the five existing packs. Import a downloaded archive, then **select it separately**; importing alone does not make it active:

```sh
PET="/path/to/herdr-desktop-pet"
"$PET" pack import --path "/absolute/path/to/chaerin-research-v0.0.6.herdrchar"
"$PET" pack select chaerin-research
```

Replace `PET` and the archive path with actual local paths, or use the app's Characters tab to import the archive and **Apply** the selected character. Use the selection ID above for another pack. Import is opt-in; this release does not replace the bundled default.

## Recreate the source fixture

The two original utilities use the Python standard library and require no asset service or third-party artwork. Run from this repository's root:

```sh
python3 tools/generate-character.py --output sources/legacy-png
python3 tools/generate-character-examples.py --output packs/png-example --replace
```

The first command recreates the original legacy four-pose raster fixture; the second recreates the v4 Coding Cat example pack from the drawing utility. `--replace` is required when `packs/png-example` already exists; do not use it on a pack with local modifications you want to keep.

## Build the catalog and gallery

To package and validate all six packs and render native previews, supply Herdr Desktop Pet **v0.3.4 or newer** and a source checkout containing `tools/character-pack.py`. Older versions remain suitable for the other five packs, but cannot establish Chaerin side-owned eye-clipping compatibility. Install the gallery image dependency:

```sh
python3 -m pip install -r requirements-gallery.txt
python3 scripts/build-catalog.py --native /absolute/path/to/herdr-desktop-pet --app-source /absolute/path/to/herdr-pet
python3 scripts/build-gallery.py
```

Both builders discover `packs/*/manifest.json`. `build-catalog.py` packages every explicitly published variant in `catalog.source.json`, validates both source and exact archive with the native app, renders five native previews per pack (`chaerin-research-idle.png` and `chaerin-research-running-0.png` through `-3.png` for Chaerin), and regenerates `catalog.json` and `SHA256SUMS` only after all packs succeed. `build-gallery.py` stages the downloads and notices; `fetch-downloads.py` verifies all pinned archive sizes and hashes. A newly discovered source-only pack has no archive without separate authorization and registration; its Pillow composite preview is not native compatibility proof.

Curated [`previews/coding-cat-profile.png`](previews/coding-cat-profile.png) and [`previews/arin-research-profile.png`](previews/arin-research-profile.png) remain unchanged during regeneration. Chaerin's [`native profile`](previews/chaerin-research-profile.png) was visually reviewed and derived from the actual v0.3.4 [`waiting idle preview`](previews/chaerin-research-idle.png), SHA-256 `598c5a0feaf36312e2550a338ea16ebe3d36ce57ea30e1baa903c6e18268f56f`, crop `[300, 0, 790, 445]`, resized with LANCZOS to 512×512 RGBA; output SHA-256 `34cb9ce0008f6436f9be406cc1e7cdbe046044de305a1d93d8f33c9db6b88dc4`. No repainting or new generation. The packaged current-ABI SDK review covered 233 actual frames: ten entries, three same-context reentries, all 80 authored clips and 140 isolated eye/mouth/head control frames. All 31 PSD/override/motion/rig-entry files remain byte-exact to the approved production source; diagnostic motion copies are not distributed. [Source provenance](packs/chaerin-research/source-record.json), [owner approval](packs/chaerin-research/owner-approval.json) and [QA policy](packs/chaerin-research/qa-release-policy.json) distinguish historical private QA from this public scope. Historical cancelled/disconnected white-eye transient cause is unresolved; the independent opposite-side/late-white regression failed before and passed all five actual-Metal fixtures on the v0.3.4 candidate. No commercial, general sublicensing or model-material rights are granted.

**Burgundy Uniform 0.0.5** adds the approved B short pleated skirt to all ten own poses, preserving original faces, earrings and motion. The actual native review covered 71 captures, with light/dark visual inspection and ten pixel-identical original face/earring regions. The owner separately confirmed original/reference redistribution rights and authorized public catalog/source/archive release; see [owner approval](packs/rubelia-burgundy-uniform/owner-approval.json). Earlier local-only notices are labeled historical. Private execution audits and authoring images are not packaged; their hashes and current source chain remain in [source provenance](packs/rubelia-burgundy-uniform/source-record.json). No new downstream commercial or model-material license is granted.

Arin **0.0.4** includes the original-portrait face repair in all ten independent native models, with the existing body artwork and eight motion slots per pose preserved. The user separately authorized this official release on 2026-10-09; [owner approvals](packs/arin-research/owner-approval.json) and the [source record](packs/arin-research/source-record.json) distinguish that authorization from operator artistic review. The standalone profile is a waiting idle t0 native capture SHA-256 `d754457b44e4bc087da1e7750322e38dc57e6042fb99ed751fa26196d2e35012`, crop `[300, 0, 720, 420]` and 512×512 LANCZOS RGBA SHA-256 `b77249f42f0b094f8284e50707ec0a61c1fb7c7235d7b9b486d5e90d7ed58d35`. The catalog's Arin idle/running previews are regenerated from the repaired production model. Historical `packs-v0.0.3` archives are not overwritten, and StageR3/91d756 records are not current face-match evidence. This release grants no new commercial or model-material rights.

Coding Cat profile provenance: source [`previews/coding-cat-idle.png`](previews/coding-cat-idle.png), SHA-256 `35df3d4346005167b645e0997723ad2e59404729fc895518733fe83629aa286d` (384×512 RGBA); face-centered square crop `[84, 35, 300, 251]` in source pixels (left, top, right, bottom), resized with LANCZOS to 512×512 RGBA PNG. Output [`previews/coding-cat-profile.png`](previews/coding-cat-profile.png) has SHA-256 `aa75304d0c0e7d570dc39465ccec8fc7af369efbbff970119e15f228a900ea3a`. Source transparency is retained; no AI generation, retouching, or new background. Rights remain unchanged: original repository-authored artwork, MIT, as recorded in [`packs/png-example/SOURCE.txt`](packs/png-example/SOURCE.txt).

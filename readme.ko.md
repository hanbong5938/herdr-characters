# Herdr 캐릭터

[English](readme.md)

이 공개 캐릭터 라이브러리의 **`packs-v0.0.4`에는 얼굴을 수정한 아린 0.0.4와 코딩 캣·루벨리아(교복)·루벨리아(수영복) 네 팩이 포함됩니다.** 다른 세 팩은 **0.0.3 버전과 기존 아카이브 바이트를 그대로 유지합니다.** **Herdr Desktop Pet v0.2.1 이상**을 사용하세요. v0.2.0은 아린의 참조 전용 mesh 레이어를 처리하지 못합니다. 코딩 캣은 오리지널 MIT 라이선스의 384×512 투명 PNG 팩(v4)이며 상태 클립 네 개와 반응 클립 네 개를 포함합니다. 나머지는 독립 포즈 10개를 가진 rig 팩(v5)이며 별도 작품 이용 조건을 유지합니다. 저장소 [MIT 라이선스](LICENSE.txt)가 이 작품을 재라이선스하지 않습니다.

## 캐릭터 미리보기

<table>
  <tr>
    <td align="center" width="180"><a href="previews/coding-cat-profile.png"><img src="previews/coding-cat-profile.png" alt="코딩 캣 프로필 미리보기" width="160"></a><br><strong>코딩 캣</strong><br>선택 다운로드<br>MIT</td>
    <td align="center" width="180"><a href="previews/arin-research-profile.png"><img src="previews/arin-research-profile.png" alt="아린 프로필 미리보기" width="160"></a><br><strong>아린</strong><br>다운로드 가능한 rig 팩<br>별도 작품 이용 조건</td>
    <td align="center" width="180"><a href="previews/rubelia-school-uniform-idle.png"><img src="previews/rubelia-school-uniform-idle.png" alt="루벨리아 교복 미리보기" width="160"></a><br><strong>루벨리아(교복)</strong><br>다운로드 가능한 rig 팩</td>
    <td align="center" width="180"><a href="previews/rubelia-white-bikini-idle.png"><img src="previews/rubelia-white-bikini-idle.png" alt="루벨리아 수영복 미리보기" width="160"></a><br><strong>루벨리아(수영복)</strong><br>다운로드 가능한 rig 팩</td>
  </tr>
</table>

아린과 루벨리아 두 복장 팩의 출처 기록은 [`shared-world-canon`](https://github.com/hanbong5938/shared-world-canon)의 원본 해시와 소유자 기록을 보존합니다. 이번 공개 다운로드·설치형 릴리스에 대한 소유자의 별도 승인은 각 팩의 `owner-approval.json`에 기록됩니다. 새 상업 이용 라이선스·독립적인 법적 권리 검증·모델 자료 이용권을 부여하지 않습니다. 라이선스·저작자·출처 고지문을 아카이브와 함께 보존하세요.

## 웹 갤러리 둘러보기

[갤러리](https://hanbong5938.github.io/herdr-characters/)는 모든 `packs/*/manifest.json`을 발견하며 [`catalog.source.json`](catalog.source.json)이 프로필과 명시적인 게시 정보를 제공합니다. 현재 네 항목 모두 다운로드할 수 있습니다. **Rig**에는 아린과 루벨리아 두 팩, **PNG**에는 코딩 캣이 표시됩니다. **연구(Research)**는 소스 전용 항목용이며 현재 해당 항목은 없습니다. 한글 이름·태그·설명·변형 이름으로 검색하고 기록된 게시 날짜 또는 이름으로 정렬할 수 있습니다. 새 소스의 자동 발견은 릴리스 승인이 아닙니다. 원본 [`sources/legacy-png`](sources/legacy-png)는 코딩 캣 소스이지 다섯 번째 팩이 아닙니다.

로컬 미리보기는 이미지 의존성을 설치하고 고정 릴리스의 네 아카이브를 가져온 다음 정적 사이트를 빌드해 실행하세요.

```sh
python3 -m pip install -r requirements-gallery.txt
python3 scripts/fetch-downloads.py
python3 scripts/build-gallery.py
npm run preview
```

`http://127.0.0.1:4187/`을 여세요. fetch는 Python 표준 라이브러리로 모든 고정 아카이브의 바이트 수와 SHA-256을 `catalog.json`과 대조합니다. 갤러리 빌드는 `dist/gallery`를 생성하며 두 명령 모두 네이티브 앱이 필요하지 않습니다. 아래 네이티브 저작 명령이 아카이브·애니메이션 미리보기를 재생성하고 Pages CI는 이미 게시된 릴리스만 가져옵니다. 갤러리는 좁은 모바일 화면과 카탈로그 오류 후 언어 전환 시 오류·재시도 상태 유지를 지원합니다.

## GitHub Pages에 게시하기

공개 갤러리는 **[https://hanbong5938.github.io/herdr-characters/](https://hanbong5938.github.io/herdr-characters/)**입니다. GitHub Pages는 **GitHub Actions**와 `github-pages` 환경을 사용합니다. **새 카탈로그를 `main`에 푸시하기 전에 모든 릴리스 파일을 게시하세요.** Pages 워크플로는 고정된 네 아카이브를 가져와 검증하고 `dist/gallery`를 빌드·배포합니다. 소스 전용 미리보기·저장소 링크가 설치형 릴리스를 승인하지는 않습니다.

## 루벨리아 복장 소스

교복·수영복 소스는 비공개 보관소에서 이 공통 저장소로 이동했습니다. 원화·10포즈 PSD·리깅·모션은 그대로이며, 공개 승인·라이선스·출처 고지문에 소유자가 승인한 `packs-v0.0.3` 다운로드 범위를 기록했습니다.

| 한국어 이름 | 영어 표시 | 원본 팩 |
| --- | --- | --- |
| 루벨리아(교복) | Rubelia (School Uniform) | [`packs/rubelia-school-uniform`](packs/rubelia-school-uniform) |
| 루벨리아(수영복) | Rubelia (Swimsuit) | [`packs/rubelia-white-bikini`](packs/rubelia-white-bikini) |

과거 소스 전용 이동에서는 설치형 아카이브를 게시하지 않았습니다. 이후 사용자가 네 팩 전체의 다운로드 릴리스를 승인했으며 루벨리아 두 팩의 `owner-approval.json`에 이 별도 승인을 기록했습니다. `NOTICE.txt`, `LICENSE.txt`, `QWEN_RESEARCH_LICENSE.txt`에 원본·모델 출처를 보존하고 새 상업 이용 라이선스는 부여하지 않습니다.

비공개 로컬 갤러리는 같은 원본을 참조해 위 한·영 이름을 표시합니다. 앱에 설치되는 manifest 이름은 한국어 단일 문자열이며 앱 언어에 따른 자동 이름 전환은 지원하지 않습니다.

## 다운로드 및 가져오기

[`packs-v0.0.4`](https://github.com/hanbong5938/herdr-characters/releases/tag/packs-v0.0.4)에서 네 아카이브와 [`SHA256SUMS`](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.4/SHA256SUMS)를 받으세요. 수정된 아린 0.0.4와 변경 없는 다른 세 팩의 0.0.3 아카이브를 포함합니다. 과거 `packs-v0.0.3`과 코딩 캣만 포함한 `packs-v0.0.2` 릴리스는 변경하지 않습니다.

| 캐릭터 | 아카이브 | 선택 ID |
| --- | --- | --- |
| 코딩 캣 | [coding-cat-v0.0.3.herdrchar](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.4/coding-cat-v0.0.3.herdrchar) | `coding-cat` |
| 아린 | [arin-research-v0.0.4.herdrchar](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.4/arin-research-v0.0.4.herdrchar) | `arin-research` |
| 루벨리아(교복) | [rubelia-school-uniform-v0.0.3.herdrchar](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.4/rubelia-school-uniform-v0.0.3.herdrchar) | `rubelia-school-uniform` |
| 루벨리아(수영복) | [rubelia-white-bikini-v0.0.3.herdrchar](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.4/rubelia-white-bikini-v0.0.3.herdrchar) | `rubelia-white-bikini` |

네 파일과 `SHA256SUMS`를 같은 폴더에 내려받아 `shasum -a 256 -c SHA256SUMS`로 검증하세요. [`catalog.json`](catalog.json)에도 각 아카이브의 정확한 바이트 수와 SHA-256이 기록됩니다.

[v0.2.1 앱](https://github.com/hanbong5938/herdr-desktop-pet/releases/tag/v0.2.1) 이상으로 가져온 **다음 별도로 선택**하세요. 가져오기만 해서는 활성화되지 않습니다.

```sh
PET="/path/to/herdr-desktop-pet"
"$PET" pack import --path "/absolute/path/to/arin-research-v0.0.4.herdrchar"
"$PET" pack select arin-research
```

`PET`와 아카이브 경로를 실제 로컬 경로로 바꾸거나 앱의 **캐릭터** 탭에서 가져온 뒤 선택한 캐릭터를 **적용**하세요. 다른 팩은 위 표의 선택 ID를 사용합니다. 안정판 v0.2.1은 수동 가져오기를 지원하며 `main`의 미출시 온라인 캐릭터 브라우저를 포함하거나 내장 기본 캐릭터를 교체하지 않습니다.

## 소스 예제 다시 생성하기

오리지널 도구 두 개는 Python 표준 라이브러리만 사용하며 외부 에셋 서비스나 타사 그림이 필요하지 않습니다. 이 저장소의 루트에서 실행하세요.

```sh
python3 tools/generate-character.py --output sources/legacy-png
python3 tools/generate-character-examples.py --output packs/png-example --replace
```

첫 번째 명령은 원본 네 포즈 레거시 래스터 예제를, 두 번째 명령은 그림 생성 도구를 이용한 v4 코딩 캣 예제 팩을 다시 만듭니다. 기존 `packs/png-example` 폴더를 교체하려면 `--replace`가 필요합니다. 보존해야 할 로컬 변경 사항이 있다면 실행하지 마세요.

## 카탈로그와 갤러리 빌드

네 팩을 모두 패키징·검증하고 네이티브 미리보기를 렌더링하려면 **Herdr Desktop Pet v0.2.1 이상**과 `tools/character-pack.py`가 있는 소스 체크아웃을 제공하세요. 갤러리 이미지 의존성을 설치하세요.

```sh
python3 -m pip install -r requirements-gallery.txt
python3 scripts/build-catalog.py --native /absolute/path/to/herdr-desktop-pet --app-source /absolute/path/to/herdr-pet
python3 scripts/build-gallery.py
```

두 빌더 모두 `packs/*/manifest.json`을 발견합니다. `build-catalog.py`는 `catalog.source.json`에 명시적으로 게시한 모든 변형을 패키징하고, 소스와 정확한 아카이브를 네이티브 앱으로 검증한 뒤 팩마다 네이티브 미리보기 다섯 장을 렌더링합니다. 모든 팩이 성공한 뒤에만 `catalog.json`과 `SHA256SUMS`를 갱신합니다. `build-gallery.py`는 현재 네 다운로드와 이용 고지를 배치하며 `fetch-downloads.py`는 모든 고정 아카이브의 크기·해시를 확인합니다. 새 소스 전용 팩은 별도 승인·등록 전까지 아카이브가 없으며 Pillow 합성 미리보기가 네이티브 호환성 증명은 아닙니다.

카탈로그 재생성은 기존 [`previews/coding-cat-profile.png`](previews/coding-cat-profile.png)와 [`previews/arin-research-profile.png`](previews/arin-research-profile.png)를 보존합니다. 아린의 [출처 기록](packs/arin-research/source-record.json)과 [소유자 승인](packs/arin-research/owner-approval.json)은 과거 프로필·소스 전용 범위를 이후 공개 팩 릴리스 승인과 구분합니다. 다운로드 카탈로그는 내장 캐릭터를 추가하거나 상업 이용·모델 자료 이용권을 부여하지 않습니다.

아린 **0.0.4**에는 원본 초상화를 기준으로 수정한 얼굴이 독립 native 모델 10개 모두에 포함됩니다. 기존 비얼굴 원화와 포즈별 모션 8개는 유지합니다. 사용자가 2026-10-09 공식 배포를 별도로 요청했으며 [소유자 승인](packs/arin-research/owner-approval.json)과 [출처 기록](packs/arin-research/source-record.json)은 그 승인과 운영자의 시각 검토를 구분합니다. 독립 프로필은 waiting idle t0 네이티브 캡처 SHA-256 `d754457b44e4bc087da1e7750322e38dc57e6042fb99ed751fa26196d2e35012`에서 `[300, 0, 720, 420]`을 잘라 LANCZOS로 512×512 RGBA 크기로 만든 결과이며 SHA-256은 `b77249f42f0b094f8284e50707ec0a61c1fb7c7235d7b9b486d5e90d7ed58d35`입니다. 카탈로그의 아린 대기·작업 미리보기도 수정된 production 모델로 재생성합니다. 과거 `packs-v0.0.3` 아카이브는 덮어쓰지 않으며 StageR3/91d756 기록은 현재 얼굴 일치성의 근거가 아닙니다. 이번 배포는 새 상업 이용·모델 자료 이용권을 부여하지 않습니다.

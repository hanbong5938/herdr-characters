# Herdr 캐릭터

[English](readme.md)

이 공개 캐릭터 라이브러리에서는 현재 **코딩 캣(Coding Cat)만** 제공합니다. Herdr Desktop Pet용 오리지널 MIT 라이선스 절차적 PNG 캐릭터 팩입니다. 캐릭터 포맷은 v4이고 투명한 384×512 PNG 프레임, 상태 클립 네 개(idle, running, waiting, unknown), 반응 클립 네 개(head tap, body tap, pet, completion observed)를 포함합니다. 팩과 출처 고지문은 [`packs/png-example`](packs/png-example), 재현 가능한 그림 생성 도구는 [`tools/generate-character.py`](tools/generate-character.py)에 있습니다. 저장소의 [MIT 라이선스](LICENSE.txt)는 오리지널 소스 도구와 예제 파일에 적용됩니다.

## 다운로드 및 가져오기

공개 `packs-v0.0.2` 릴리스에서 [`coding-cat-v0.0.2.herdrchar`](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.2/coding-cat-v0.0.2.herdrchar)와 [`SHA256SUMS`](https://github.com/hanbong5938/herdr-characters/releases/download/packs-v0.0.2/SHA256SUMS)를 다운로드하세요. 다운로드한 파일이 있는 폴더에서 `shasum -a 256 -c SHA256SUMS`로 아카이브를 검증할 수 있습니다. 생성된 [`catalog.json`](catalog.json)에도 정확한 바이트 수와 SHA-256 해시가 기록됩니다. 이 문서에 임의의 해시값을 사용하지 않습니다.

Herdr Desktop Pet 네이티브 실행 파일로 아카이브를 가져온 **다음 별도로 선택**하세요. 가져오기만 해서는 활성화되지 않습니다.

```sh
PET="/path/to/herdr-desktop-pet"
"$PET" pack import --path "/absolute/path/to/coding-cat-v0.0.2.herdrchar"
"$PET" pack select coding-cat
```

`PET`와 아카이브 경로를 실제 로컬 경로로 바꾸세요. 또는 앱의 **캐릭터** 탭에서 아카이브를 가져오고 코딩 캣을 선택한 뒤 **적용**을 누르세요.

## 소스 예제 다시 생성하기

오리지널 도구 두 개는 Python 표준 라이브러리만 사용하며 외부 에셋 서비스나 타사 그림이 필요하지 않습니다. 이 저장소의 루트에서 실행하세요.

```sh
python3 tools/generate-character.py --output sources/legacy-png
python3 tools/generate-character-examples.py --output packs/png-example --replace
```

첫 번째 명령은 원본 네 포즈 레거시 래스터 예제를, 두 번째 명령은 그림 생성 도구를 이용한 v4 코딩 캣 예제 팩을 다시 만듭니다. 기존 `packs/png-example` 폴더를 교체하려면 `--replace`가 필요합니다. 보존해야 할 로컬 변경 사항이 있다면 실행하지 마세요.

## 카탈로그와 갤러리 빌드

예제를 패키징·검증하고 갤러리 미리보기를 렌더링하려면 Herdr 네이티브 실행 파일과 `tools/character-pack.py`가 있는 Herdr Desktop Pet 소스 체크아웃을 제공하세요.

```sh
python3 scripts/build-catalog.py --native /absolute/path/to/herdr-desktop-pet --app-source /absolute/path/to/herdr-pet
python3 scripts/build-gallery.py
```

`build-catalog.py`는 [`catalog.source.json`](catalog.source.json)을 읽어 `catalog.json`, `downloads/coding-cat-v0.0.2.herdrchar`, `downloads/SHA256SUMS`, 네이티브 미리보기 이미지 다섯 장을 생성합니다. `build-gallery.py`는 아카이브를 생성된 카탈로그와 대조한 뒤 정적 사이트를 `dist/gallery`에 준비합니다. 로컬에서 패키징하지 않고 **이미 게시된** 공개 릴리스 파일을 익명으로 받으려면 해당 릴리스에 맞게 생성된 `catalog.json`을 확보하고 `python3 scripts/fetch-downloads.py`, `python3 scripts/build-gallery.py` 순으로 실행하세요. fetch 스크립트는 바이트 수 또는 SHA-256이 카탈로그와 다른 아카이브를 거부합니다. 다운로드한 아카이브로 갤러리를 빌드할 때는 미리보기 이미지가 로컬에 이미 있어야 합니다.

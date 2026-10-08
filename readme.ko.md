# Herdr 캐릭터

[English](readme.md)

이 공개 캐릭터 라이브러리에서 **다운로드할 수 있는 팩은 코딩 캣(Coding Cat)뿐**이며, 아린(Arin)의 공개 프로필 미리보기와 [연구용 소스 파일](packs/arin-research)도 저장소에 공개됩니다. 아린의 공식 패키지 릴리스는 없습니다. 코딩 캣은 Herdr Desktop Pet용 오리지널 MIT 라이선스 절차적 PNG 캐릭터 팩입니다. 캐릭터 포맷은 v4이고 투명한 384×512 PNG 프레임, 상태 클립 네 개(idle, running, waiting, unknown), 반응 클립 네 개(head tap, body tap, pet, completion observed)를 포함합니다. 팩과 출처 고지문은 [`packs/png-example`](packs/png-example), 재현 가능한 그림 생성 도구는 [`tools/generate-character.py`](tools/generate-character.py)에 있습니다. 저장소의 [MIT 라이선스](LICENSE.txt)는 오리지널 소스 도구와 예제 파일에 적용됩니다.

## 캐릭터 미리보기

<table>
  <tr>
    <td align="center" width="180"><a href="previews/coding-cat-profile.png"><img src="previews/coding-cat-profile.png" alt="코딩 캣 프로필 미리보기" width="160"></a><br><strong>코딩 캣</strong><br>선택 다운로드<br>MIT</td>
    <td align="center" width="180"><a href="previews/arin-research-profile.png"><img src="previews/arin-research-profile.png" alt="아린 연구용 프로필 미리보기" width="160"></a><br><strong>아린</strong><br>프로필 미리보기<br>팩 릴리스 없음</td>
  </tr>
</table>

코딩 캣은 다운로드할 수 있는 선택형 [MIT 라이선스 팩](packs/png-example/SOURCE.txt)입니다. 아린의 [소유자 승인 기록](packs/arin-research/owner-approval.json)은 프로필 공개 표시와 PSD를 포함한 [저장소의 연구용 소스](packs/arin-research) 공개를 허용합니다. 아린의 공식 아카이브·카탈로그 다운로드·설치형 릴리스는 없으며, 아린 작품에는 별도의 [연구용 이용 조건](packs/arin-research/LICENSE.txt)이 적용됩니다.

## 루벨리아 복장 소스

교복·수영복의 현재 원본 팩은 비공개 보관소에서 이 공통 저장소로 이동했습니다. 원화·10포즈 PSD·리깅·모션은 그대로이며, 이름과 저장소 소스 공개 범위만 갱신했습니다.

| 한국어 이름 | 영어 표시 | 원본 팩 |
| --- | --- | --- |
| 루벨리아(교복) | Rubelia (School Uniform) | [`packs/rubelia-school-uniform`](packs/rubelia-school-uniform) |
| 루벨리아(수영복) | Rubelia (Swimsuit) | [`packs/rubelia-white-bikini`](packs/rubelia-white-bikini) |

사용자는 두 팩을 공개 저장소 소스로 포함하는 범위를 선택했습니다. 각 팩의 `owner-approval.json`에 이 사용자 진술을 기록하며, 독립적인 권리 검증이나 새 모델 라이선스를 뜻하지 않습니다. 원본·Qwen 이용 조건은 각 팩의 `NOTICE.txt`, `LICENSE.txt`, `QWEN_RESEARCH_LICENSE.txt`를 따릅니다. 이번 이동으로 commit·push·공식 패키지 릴리스를 수행하지 않았으며, 공개 다운로드 카탈로그에는 추가하지 않았습니다.

비공개 로컬 갤러리는 같은 원본을 참조해 위 한·영 이름을 표시합니다. 앱에 설치되는 manifest 이름은 한국어 단일 문자열이며 앱 언어에 따른 자동 이름 전환은 지원하지 않습니다.


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

저장소의 독립 프로필 이미지에는 코딩 캣의 기존 기본 idle 이미지로 만든 [`previews/coding-cat-profile.png`](previews/coding-cat-profile.png)와 아린의 네이티브 waiting 렌더에서 잘라낸 [`previews/arin-research-profile.png`](previews/arin-research-profile.png)가 있습니다(출처 기록: [`packs/arin-research/source-record.json`](packs/arin-research/source-record.json)). 소유자가 진술한 공개 프로필 표시 및 저장소 소스 공개 승인과 날짜는 [`packs/arin-research/owner-approval.json`](packs/arin-research/owner-approval.json)에 기록됩니다. 이 진술은 독립적으로 확인된 법적 허가가 아니며 공식 패키지 릴리스, 상업적 사용, 모델 자료의 이용권이나 앱 카탈로그·캐릭터 메뉴 등록을 허용하지 않습니다. 카탈로그를 다시 생성해도 프로필 PNG는 보존되며 카탈로그나 생성된 갤러리에는 추가되지 않습니다.

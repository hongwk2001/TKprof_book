# 🎙️ 베오울프 한국어 오디오북 — 제작 레퍼런스 문서

**프로젝트**: Beowulf Korean Audiobook  
**버전**: v1.0  
**최종 업데이트**: 2026-07-06  
**작업 디렉토리**: `D:\git_repo\TKprof_book\books\beowulf\`

---

## 목차
1. [프로젝트 현황](#1-프로젝트-현황)
2. [전체 파이프라인 흐름도](#2-전체-파이프라인-흐름도)
3. [Stage 1 — Korean Script JSON 생성](#3-stage-1--korean-script-json-생성)
4. [Stage 2 — 한국어 다중 음성 시스템](#4-stage-2--한국어-다중-음성-시스템)
5. [Stage 3 — Gemini 한국어 대화 태깅](#5-stage-3--gemini-한국어-대화-태깅)
6. [Stage 4 — 오디오 생성 스크립트](#6-stage-4--오디오-생성-스크립트)
7. [Stage 5 — QA 체크리스트](#7-stage-5--qa-체크리스트)
8. [Stage 6 — 파트 병합 (≤40분)](#8-stage-6--파트-병합-40분)
9. [Stage 7 — 발행](#9-stage-7--발행)
10. [파일 구조 맵](#10-파일-구조-맵)
11. [설치 요구사항](#11-설치-요구사항)
12. [진행 현황 트래커](#12-진행-현황-트래커)

---

## 1. 프로젝트 현황

### 완료된 자산 ✅

| 자산 | 경로 | 상태 |
|------|------|------|
| 한국어 챕터 텍스트 (44개 + 서문 + 저작권) | `chapters_kr_v2/` | ✅ 완료 |
| 한국어 이북 v2 | `beowulf_ko_v2.epub` | ✅ 완료 |
| 영어 오디오 생성 파이프라인 | `generate_audio.py` | ✅ 레퍼런스용 |
| 영어 Script JSON (46개) | `scripts/` | ✅ 포맷 레퍼런스 |
| 시네마틱 범퍼 MP3 | `../the_prince/freesound_community-cinematic-intro-6097.mp3` | ✅ 재사용 |
| ffmpeg / soundfile / pydub / kokoro-onnx 환경 | WSL venv | ✅ 설치됨 |

### 새로 생성할 파일 🔨

| 파일 | 역할 |
|------|------|
| `tag_dialogue_ko.py` | Gemini로 한국어 대화 태깅 |
| `prepare_scripts_ko.py` | 태깅된 텍스트 → `scripts_ko/` JSON |
| `generate_audio_ko.py` | edge-tts로 MP3 생성 |
| `scripts_ko/` (폴더) | 46개 한국어 Script JSON |
| `final_audio_ko/` (폴더) | 46개 MP3 트랙 출력 |
| `final_audio_ko/merged/` (폴더) | 최종 4파트 병합 MP3 |

---

## 2. 전체 파이프라인 흐름도

```
chapters_kr_v2/
  ch_00_ko.txt ~ ch_43_ko.txt
  introduction_ko_v2.txt
  copyright_ko_v2.txt
        │
        ▼
[ Stage 1 ] tag_dialogue_ko.py
  Gemini로 한국어 대화 태깅
  → chapters_kr_v2/tagged/tagged_ch_NN_ko.txt
        │
        ▼
[ Stage 2 ] prepare_scripts_ko.py
  태깅 텍스트를 파싱 → 목소리 배정
  → scripts_ko/script_ch_NN.json
        │
        ▼
[ Stage 3 ] generate_audio_ko.py
  edge-tts로 각 JSON 세그먼트 → WAV
  pydub으로 믹싱 → 256k MP3
  → final_audio_ko/final_track_NN.mp3 (46개)
        │
        ▼
[ Stage 4 ] QA 청취 검수
        │
        ▼
[ Stage 5 ] ffmpeg concat
  → final_audio_ko/merged/
      beowulf_ko_part1.mp3  (~38분)
      beowulf_ko_part2.mp3  (~39분)
      beowulf_ko_part3.mp3  (~39분)
      beowulf_ko_part4.mp3  (~8분)
        │
        ▼
[ Stage 6 ] Publish
```

---

## 3. Stage 1 — Korean Script JSON 생성

### 3-A. Gemini 한국어 대화 태깅 (`tag_dialogue_ko.py`)

영어판의 `tag_dialogue.py`를 한국어용으로 새로 작성.

**입력**: `chapters_kr_v2/ch_NN_ko.txt`  
**출력**: `chapters_kr_v2/tagged/tagged_ch_NN_ko.txt`

**Gemini 시스템 프롬프트 (한국어용)**:
```
당신은 베오울프 한국어판의 대화를 태깅하는 전문 문학 어시스턴트입니다.
각 챕터에서 실제 발화된 대사를 찾아 XML 스타일 화자 태그로 감쌉니다.
모든 나레이션 텍스트는 절대 수정하지 않습니다.

사용 가능한 태그:
- <베오울프>...</베오울프>    : 베오울프의 대사
- <흐로스가르>...</흐로스가르> : 흐로스가르 왕의 대사
- <위글라프>...</위글라프>   : 위글라프의 대사
- <기타>...</기타>           : 그 외 모든 화자 (경비병, 전령, 운페르스 등)

규칙:
1. 실제 발화된 대사(큰따옴표 내부)만 태그로 감쌉니다.
2. 나레이션, 묘사 문장은 절대 수정하지 않습니다.
3. 원문의 단 한 글자도 추가/삭제/수정하지 않습니다.
4. 마크다운 블록 없이 전체 챕터를 그대로 반환합니다.
```

> [!IMPORTANT]
> **API 미사용 알림**: 본 단계는 외부 Gemini API 직접 호출을 사용하는 대신, **챗창 내부 또는 서브에이전트(LLM)**를 호출하여 한국어 대화를 태깅하는 방식을 취합니다. 
> 
> **대화 태깅 프로세스**:
> 1. 서브에이전트가 `chapters_kr_v2/`에서 텍스트를 순차적으로 로드.
> 2. 내부 LLM 연산을 통해 태그가 지정된 버전을 생성.
> 3. 이를 직접 `chapters_kr_v2/tagged/tagged_ch_NN_ko.txt`에 기록.
> 
> 이 방식은 API Key 종속성 및 쿼타 제한 오류를 회피하기 위해 채택되었습니다.

---

### 3-B. Script JSON 변환 (`prepare_scripts_ko.py`)

**입력**: `chapters_kr_v2/tagged/tagged_ch_NN_ko.txt`  
**출력**: `scripts_ko/script_ch_NN.json`

태그 → 목소리 매핑 (아래 섹션 4 참고).

**특수 파일**:
- `introduction_ko_v2.txt` → `scripts_ko/script_intro.json` (내레이터만)
- `copyright_ko_v2.txt` → `scripts_ko/script_closing.json` (내레이터만)

---

## 4. Stage 2 — 한국어 다중 음성 시스템

### TTS 엔진: edge-tts (Microsoft Neural)

**선택 이유**:
- Kokoro ONNX는 현재 한국어 음질이 불안정 (실험적 단계)
- edge-tts는 Microsoft Azure 품질의 신경망 한국어 음성 — 무료, 안정적
- `pip install edge-tts`로 간단 설치

### 3개 한국어 음성 배역 및 속도 연출

| 역할 | 화자 | edge-tts 음성 ID | 성별 | 음색 및 연출 설정 |
|------|------|-----------------|------|-----------|
| **내레이터** | 나레이션 전체 | `ko-KR-InJoonNeural` | 남성 | 중후하고 차분한 기본 속도 (`+0%`) |
| **베오울프** | 베오울프 대사 | `ko-KR-HyunsuMultilingualNeural` | 남성 | 젊고 힘찬 전사 캐릭터 묘사 (`+5%`) |
| **흐로스가르** | 흐로스가르 대사 | `ko-KR-InJoonNeural` | 남성 | 나레이터 음성을 느린 속도로 낮추어 노왕의 위엄 표현 (`-12%`) |
| **위글라프 / 기타** | 위글라프 + 기타 대사 | `ko-KR-HyunsuMultilingualNeural` | 남성 | 힘있는 젊은 전사 음색 (`+0%`) |
| **여왕 / 여성** | 웰테오 왕비 등 | `ko-KR-SunHiNeural` | 여성 | 맑고 부드러운 왕비 음색 (`+0%`) |

---

### 태그 → 음성 매핑 딕셔너리

```python
VOICE_MAP = {
    "narrator":   ("ko-KR-InJoonNeural", "+0%"),
    "베오울프":    ("ko-KR-HyunsuMultilingualNeural", "+5%"),
    "흐로스가르":  ("ko-KR-InJoonNeural", "-12%"),
    "위글라프":    ("ko-KR-HyunsuMultilingualNeural", "+0%"),
    "기타":        ("ko-KR-HyunsuMultilingualNeural", "+0%"),
    "여성":        ("ko-KR-SunHiNeural", "+0%"),
}
```

### Script JSON 포맷 예시

```json
[
  {
    "character": "narrator",
    "voice": "ko-KR-InJoonNeural",
    "speed": "+0%",
    "text": "제5장: 베오울프의 도전\n\n어둠이 물러가고 새벽빛이 번질 무렵..."
  },
  {
    "character": "흐로스가르",
    "voice": "ko-KR-BongJinNeural",
    "speed": "-5%",
    "text": "드디어 도움이 왔구나. 그대의 이름과 가문을 밝혀라."
  },
  {
    "character": "베오울프",
    "voice": "ko-KR-HyunsuNeural",
    "speed": "+5%",
    "text": "저는 히옐라크의 부하 베오울프입니다. 제 주군께 이 소문을 전해들었습니다."
  }
]
```

---

## 5. Stage 3 — Gemini 한국어 대화 태깅

### 베오울프 주요 화자 목록

| 한국어 이름 | 등장 챕터 | 대사 빈도 |
|------------|---------|---------|
| 베오울프 | 5, 7, 8, 9, 26, 36, 37, 39 | ★★★★★ |
| 흐로스가르 | 5, 8, 12, 26, 27 | ★★★★ |
| 위글라프 | 36, 37, 38, 39, 40 | ★★★ |
| 기타 (경비대장, 전령, 운페르스, 그 외) | 산발적 | ★★ |

### 태깅 검증 로직

영어판 `tag_dialogue.py`와 동일한 검증 패턴 사용:
1. 태그 제거 후 원문과 비교 (정규화된 공백 기준)
2. 불일치 시 Dynamic Alignment 시도
3. 5회 재시도 후 실패 시 원문 그대로 반환 (나레이터 단일 처리)

---

## 6. Stage 4 — 오디오 생성 스크립트

### `generate_audio_ko.py` 핵심 설계

```python
import asyncio
import edge_tts
import os, json
import numpy as np
import soundfile as sf
from pydub import AudioSegment

SCRIPTS_DIR  = "scripts_ko/"
OUTPUT_DIR   = "final_audio_ko/"
TEMP_DIR     = "temp_audio/"
BUMPER_PATH  = "../the_prince/freesound_community-cinematic-intro-6097.mp3"
SAMPLE_RATE  = 24000
BITRATE      = "256k"

async def synthesize_segment(text, voice, speed, out_wav):
    """edge-tts로 단일 세그먼트를 WAV로 저장"""
    communicate = edge_tts.Communicate(text, voice, rate=speed)
    await communicate.save(out_wav)

async def generate_chapter(ch_arg):
    # 1. scripts_ko/script_ch_NN.json 읽기
    # 2. 각 세그먼트 → edge-tts → 임시 WAV
    # 3. WAV 합치기 (세그먼트 유형에 따른 무음 간격)
    # 4. pydub으로 44.1kHz 스테레오 업샘플링
    # 5. 시네마틱 범퍼 믹싱
    # 6. 256k MP3 내보내기
    pass
```

### 범퍼 규칙 (영어판과 동일)

| 챕터 유형 | 범퍼 처리 |
|----------|----------|
| `intro` | 시작 4.5초 음악 → 0.5초 무음 → 나레이션 |
| `closing` | 나레이션 → 0.5초 무음 → 전체 음악 |
| `ch_00` ~ `ch_43` | 시작 2.0초 음악 → 0.5초 무음 → 나레이션 |

### 세그먼트 간 무음

| 전환 유형 | 간격 |
|----------|------|
| 나레이터 → 나레이터 | 300ms |
| 나레이터 → 캐릭터 | 500ms |
| 캐릭터 → 나레이터 | 500ms |
| 캐릭터 → 캐릭터 | 400ms |

### 실행 명령 (Git Bash)

```bash
source venv/Scripts/activate
cd /d/git_repo/TKprof_book/books/beowulf

# 전체 생성 (46개 트랙)
python generate_audio_ko.py

# 개별 실행
python generate_audio_ko.py intro
python generate_audio_ko.py 00
python generate_audio_ko.py closing
```

---

## 7. Stage 5 — QA 체크리스트

초반 3개 트랙 생성 후 반드시 청취 검수:

### 발음 확인 항목

| 한국어 표기 | 확인 |
|------------|------|
| 베오울프 | ☐ |
| 흐로스가르 | ☐ |
| 그렌델 | ☐ |
| 헤오로트 | ☐ |
| 위글라프 | ☐ |
| 히옐라크 | ☐ |

### 음질 체크

- [ ] 내레이터 ↔ 캐릭터 음성 전환이 자연스러운가?
- [ ] 범퍼 음악이 나레이션을 압도하지 않는가?
- [ ] 세그먼트 간 무음 간격이 적절한가?
- [ ] 속도(`speed`)가 청취에 편안한가?
- [ ] 챕터 제목이 자연스럽게 읽히는가?
- [ ] 태그라인(`> *...*`)이 자연스럽게 읽히는가?

---

## 8. Stage 6 — 파트 병합 (≤40분)

### 병합 그룹

| 파트 | 포함 트랙 | 트랙 수 | 예상 시간 |
|------|----------|--------|----------|
| **Part 1** | intro + ch_00 ~ ch_15 | 17 | ~38분 |
| **Part 2** | ch_16 ~ ch_30 | 15 | ~39분 |
| **Part 3** | ch_31 ~ ch_42 | 12 | ~39분 |
| **Part 4** | ch_43 + closing | 2 | ~8분 |

### ffmpeg 병합 명령 (PowerShell)

```powershell
$base = "D:\git_repo\TKprof_book\books\beowulf\final_audio_ko"
New-Item -ItemType Directory -Force "$base\merged"

ffmpeg -f concat -safe 0 -i "$base\part1_ko_list.txt" -c copy "$base\merged\beowulf_ko_part1.mp3"
ffmpeg -f concat -safe 0 -i "$base\part2_ko_list.txt" -c copy "$base\merged\beowulf_ko_part2.mp3"
ffmpeg -f concat -safe 0 -i "$base\part3_ko_list.txt" -c copy "$base\merged\beowulf_ko_part3.mp3"
ffmpeg -f concat -safe 0 -i "$base\part4_ko_list.txt" -c copy "$base\merged\beowulf_ko_part4.mp3"
```

---

## 9. Stage 7 — 발행

| 항목 | 내용 |
|------|------|
| 제목 | 베오울프: 스펙터클 현대 한국어판 |
| 부제 | Beowulf: Spectacular Modern Korean Edition |
| 언어 | 한국어 (ko) |
| 파트 수 | 4 |
| 파일 형식 | MP3, 256kbps, 44.1kHz 스테레오 |

---

## 10. 파일 구조 맵

```
books/beowulf/
│
├── chapters_kr_v2/                  ← 입력 텍스트 (47개 파일)
│   ├── ch_00_ko.txt ~ ch_43_ko.txt
│   ├── introduction_ko_v2.txt
│   ├── copyright_ko_v2.txt
│   └── tagged/                      ← Gemini 태깅 결과
│       └── tagged_ch_NN_ko.txt
│
├── scripts_ko/                      ← 변환된 JSON (46개)
│   ├── script_intro.json
│   ├── script_ch_00.json ~ script_ch_43.json
│   └── script_closing.json
│
├── final_audio_ko/                  ← 생성된 MP3 (46개)
│   ├── final_track_00_intro.mp3
│   ├── final_track_00.mp3 ~ final_track_43.mp3
│   ├── closing.mp3
│   ├── part1_ko_list.txt ~ part4_ko_list.txt
│   └── merged/
│       ├── beowulf_ko_part1.mp3    (~38분)
│       ├── beowulf_ko_part2.mp3    (~39분)
│       ├── beowulf_ko_part3.mp3    (~39분)
│       └── beowulf_ko_part4.mp3    (~8분)
│
├── tag_dialogue_ko.py               ← 신규 (Gemini 한국어 태깅)
├── prepare_scripts_ko.py            ← 신규 (JSON 변환)
├── generate_audio_ko.py             ← 신규 (edge-tts 생성)
└── beowulf_korean_audio_roadmap.md  ← 이 문서
```

---

## 11. 설치 요구사항

> ⚠️ **반드시 Git Bash 터미널에서 진행**
> ```bash
> cd /d/git_repo/TKprof_book
> source venv/Scripts/activate
> ```

```bash
# edge-tts 설치
pip install edge-tts

# 한국어 음성 목록 확인
edge-tts --list-voices | grep "ko-KR"
```

**예상 출력 (사용할 3개 음성)**:
```
ko-KR-HyunsuMultilingualNeural | Male   ← 베오울프 / 위글라프 / 기타
ko-KR-InJoonNeural             | Male   ← 내레이터 / 흐로스가르 (느리게)
ko-KR-SunHiNeural              | Female   ← 여왕 / 여성
```

---

## 12. 진행 현황 트래커

| 단계 | 작업 | 상태 |
|------|------|------|
| **준비** | 한국어 챕터 텍스트 완성 | ✅ 완료 |
| **준비** | `edge-tts` 설치 | ✅ 완료 |
| **Stage 1** | `tag_dialogue_ko.py` 작성 | ✅ 완료 |
| **Stage 1** | Gemini 한국어 대화 태깅 실행 (44챕터) | 🏃 대기 (런처 실행 전) |
| **Stage 2** | `prepare_scripts_ko.py` 작성 | ✅ 완료 |
| **Stage 2** | `scripts_ko/` JSON 46개 생성 | 🏃 대기 (런처 실행 전) |
| **Stage 3** | `generate_audio_ko.py` 작성 | ✅ 완료 |
| **Stage 3** | 샘플 테스트 (intro + ch_00 ~ ch_02) | 🏃 대기 (런처 실행 전) |
| **Stage 3** | 전체 46개 트랙 생성 | 🏃 대기 (런처 실행 전) |
| **Stage 4** | QA 청취 검수 | ☐ 대기 |
| **Stage 5** | 4파트 병합 filelist 작성 | ☐ 대기 |
| **Stage 5** | ffmpeg 병합 실행 | ☐ 대기 |
| **Stage 6** | 발행 | ☐ 대기 |

---

*이 문서는 제작 과정에서 업데이트되는 살아있는 레퍼런스입니다.*

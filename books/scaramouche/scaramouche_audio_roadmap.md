# 🎙️ 스카라무슈 한국어 오디오북 — 제작 레퍼런스 및 로드맵 (Audiobook Roadmap)

**프로젝트**: Scaramouche (스카라무슈) Korean Audiobook  
**버전**: v1.0  
**작업 디렉토리**: `D:\git_repo\TKprof_book\books\scaramouche\`

---

## 📅 전체 파이프라인 흐름도

```
chapters/
  ch_01_ko.txt ~ ch_36_ko.txt
  introduction_ko.txt
  copyright_ko.txt
        │
        ▼
[ Stage 1 ] tag_dialogue_ko.py
  Gemini로 한국어 대화 태깅 및 배역 지정
  → chapters/tagged/tagged_ch_NN_ko.txt
        │
        ▼
[ Stage 2 ] prepare_scripts_ko.py
  태깅 텍스트 파싱 및 목소리 배정
  → scripts_ko/script_ch_NN.json
        │
        ▼
[ Stage 3 ] generate_audio_ko.py
  edge-tts로 각 세그먼트 생성 및 병합 (256k MP3)
  → final_audio_ko/final_track_NN.mp3
        │
        ▼
[ Stage 4 ] QA 청취 검수 및 피드백 수정
  (RMS, Peak, Silence 규격 검증)
        │
        ▼
[ Stage 5 ] ffmpeg concat 파트 병합 (≤120분 단위 파일)
  → final_audio_ko/merged/
        │
        ▼
[ Stage 6 ] 최종 발행 (Publish)
```

---

## 🎭 한국어 음성 배역 및 설정 (Microsoft Neural Voices)

*Scaramouche*의 모험, 역사, 그리고 연극(Commedia dell'arte)적 특성에 맞춘 음색 매핑:

| 역할 (Tag) | 화자 | edge-tts 음성 ID | 성별 | 음색 및 연출 속도 |
| :--- | :--- | :--- | :--- | :--- |
| **narrator** | 전체 나레이션 | `ko-KR-SunHiNeural` | 여성 | 지적이고 명확하며 흡입력 있는 나레이션 속도 (`+0%`) |
| **앙드레** | 앙드레 루이 모로 (남주) | `ko-KR-HyunsuMultilingualNeural` | 남성 | 냉소적이고 지적이며 웅변가다운 톤 속도 (`+3%`) |
| **필립** | 필립 드 빌모랭 (친구) | `ko-KR-HyunsuMultilingualNeural` | 남성 | 열정적이고 이상적인 젊은 사제 속도 (`+1%`) |
| **라투르** | 라 투르 다르지르侯 (숙적) | `ko-KR-InJoonNeural` | 남성 | 오만하고 차가우며 위압적인 귀족 톤 속도 (`-2%`) |
| **알린** | 알린 드 케르카디우 (여주) | `ko-KR-SunHiNeural` | 여성 | 우아하고 지혜로우며 감정이 풍부한 속도 (`+2%`) |
| **클리멘** | 클리멘 (첫 연인/여배우) | `ko-KR-SunHiNeural` | 여성 | 활발하고 요염하며 감정 기복이 큰 연극적 속도 (`+4%`) |
| **케르카디우** | 케르카디우 (대부) | `ko-KR-InJoonNeural` | 남성 | 나이가 있고 다소 보수적이나 따뜻한 삼촌 속도 (`-4%`) |
| **기타여성** | 귀족 부인들, 극단 인물 등 | `ko-KR-SunHiNeural` | 여성 | 역할에 맞춰 톤 및 속도 조절 (`-5%` ~ `+5%`) |
| **기타남성** | 정치인, 결투 상대, 단원 등 | `ko-KR-InJoonNeural` | 남성 | 역할에 맞춰 톤 및 속도 조절 (`-5%` ~ `+5%`) |

---

## ⚙️ 오디오 기술 사양 (Authors Republic & ACX 필수 표준)

모든 제작 파일은 다음 기술 사양을 반드시 준수하며, 생성 후 `check_audio_quality.py`를 통해 통과해야 합니다.

1. **RMS 볼륨**: **-23 dB ~ -18 dB** (권장 목표: **-19 dB**)
2. **피크 진폭**: 최대 **-3.0 dB** (클리핑 방지를 위해 **-3.1 dB ~ -3.5 dB** 타겟팅)
3. **무음 구간 (Silence Padding)**: 
   - 파일 시작 부분: **1.0 ~ 5.0초**의 깨끗한 룸 톤 무음 (디지털 제로가 아님)
   - 파일 끝 부분: **1.0 ~ 5.0초**의 깨끗한 룸 톤 무음
4. **오디오 형식**: **44,100 Hz** 샘플 레이트, **CBR 192 kbps** 이상 (권장 **256 kbps**) MP3
5. **파일 길이**: 개별 오디오 파일당 최대 **120분** 미만으로 유지

---

## 📂 파일 구조 맵 (Expected File Tree)

```
books/scaramouche/
│
├── raw_source.txt                   ← Gutenberg 원본 텍스트
├── scaramouche_roadmap.md           ← eBook 제작 로드맵
├── scaramouche_audio_roadmap.md     ← 이 문서
├── prompt.txt                       ← 현대화/번역용 프롬프트 파일
│
├── chapters/                        ← 세그먼트화된 텍스트 폴더 (예정)
│   ├── raw_ch_01.txt ~ raw_ch_36.txt
│   ├── introduction_ko.txt
│   ├── copyright_ko.txt
│   └── tagged/                      ← Stage 1: Gemini 대화 태깅 완료본
│       └── tagged_ch_NN_ko.txt
│
├── scripts/                         ← Stage 2: JSON 변환 스크립트 폴더 (예정)
│   ├── script_ch_01.json ~ script_ch_36.json
│   └── script_intro.json
│
├── temp_audio/                      ← Stage 3: 세그먼트 단위 임시 오디오 폴더
└── final_audio/                     ← Stage 3/5: 최종 트랙 및 병합본 폴더
    ├── final_track_01.mp3 ~ final_track_36.mp3
    └── merged/                      ← 최종 유통용 병합본 파트
```

---

## 🏃 진행 현황 트래커 (Progress Tracker)

| 단계 | 작업 내용 | 상태 |
| :--- | :--- | :--- |
| **준비** | 원본 텍스트 다운로드 및 디렉토리 생성 | ✅ 완료 |
| **Stage 1** | 텍스트 현대화 및 한글 번역 진행 | ⬜ 대기 |
| **Stage 2** | `tag_dialogue_ko.py` 활용 대화 태깅 진행 | ⬜ 대기 |
| **Stage 3** | JSON 변환 및 음성 매핑 검수 | ⬜ 대기 |
| **Stage 4** | `generate_audio_ko.py` 구동 및 오디오 합성 | ⬜ 대기 |
| **Stage 5** | 오디오 QA 청취 및 기술 검수 (`check_audio_quality.py` 통과) | ⬜ 대기 |
| **Stage 6** | 파트 병합 및 최종 발행 (Publish) | ⬜ 대기 |

# 🎙️ 블루 캐슬 한국어 오디오북 — 제작 레퍼런스 및 로드맵 (Audiobook Roadmap)

**프로젝트**: The Blue Castle (블루 캐슬) Korean Audiobook  
**버전**: v1.0  
**작업 디렉토리**: `D:\git_repo\TKprof_book\books\blue_castle\`

---

## 📅 전체 파이프라인 흐름도

```
chapters/
  ch_01_ko.txt ~ ch_45_ko.txt
  introduction_ko.txt
  copyright_ko.txt
        │
        ▼
[ Stage 1 ] tag_dialogue_ko.py
  Gemini로 한국어 대화 태깅
  → chapters/tagged/tagged_ch_NN_ko.txt
        │
        ▼
[ Stage 2 ] prepare_scripts_ko.py
  태깅 텍스트 파싱 및 목소리 배정
  → scripts_ko/script_ch_NN.json
        │
        ▼
[ Stage 3 ] generate_audio_ko.py
  edge-tts로 각 세그먼트 생성 및 합치기 (256k MP3)
  → final_audio_ko/final_track_NN.mp3 (47개 파일)
        │
        ▼
[ Stage 4 ] QA 청취 검수 및 피드백 수정
        │
        ▼
[ Stage 5 ] ffmpeg concat 파트 병합 (≤40분)
  → final_audio_ko/merged/
      blue_castle_ko_part1.mp3 ~ part6.mp3
        │
        ▼
[ Stage 6 ] 최종 발행 (Publish)
```

---

## 🎭 3개 한국어 음성 배역 및 설정 (Microsoft Neural Voices)

*The Blue Castle*의 로판(로맨스 판타지) 장르 특성에 맞춘 음색 매핑:

| 역할 (Tag) | 화자 | edge-tts 음성 ID | 성별 | 음색 및 연출 속도 |
| :--- | :--- | :--- | :--- | :--- |
| **narrator** | 전체 나레이션 | `ko-KR-SunHiNeural` | 여성 | 차분하고 따뜻하며 생생한 나레이션 속도 (`+0%`) |
| **발랜시** | 발랜시 스털링 (여주) | `ko-KR-SunHiNeural` | 여성 | 통통 튀고 똑 부러지는 20대 여성 속도 (`+5%`) |
| **바니** | 바니 스네이스 (남주) | `ko-KR-HyunsuMultilingualNeural` | 남성 | 낮고 차분하며 믿음직한 30대 남성 속도 (`+2%`) |
| **기타여성** | 스털링 부인, 스티클스 등 | `ko-KR-SunHiNeural` | 여성 | 다소 신경질적이고 느리며 가부장적인 노인 속도 (`-8%`) |
| **기타남성** | 벤저민 삼촌, 의사들 등 | `ko-KR-InJoonNeural` | 남성 | 권위 있고 중후한 목소리 속도 (`-5%`) |

---

## 📂 파일 구조 맵 (Expected File Tree)

```
books/blue_castle/
│
├── chapters/                        ← 입력 텍스트 (완료)
│   ├── ch_01_ko.txt ~ ch_45_ko.txt
│   ├── introduction_ko.txt
│   ├── copyright_ko.txt
│   └── tagged/                      ← Stage 1: 대화 태깅 결과물 폴더
│       └── tagged_ch_NN_ko.txt
│
├── scripts_ko/                      ← Stage 2: 변환된 JSON 스크립트 폴더
│   ├── script_intro.json
│   ├── script_ch_01.json ~ script_ch_45.json
│   └── script_closing.json
│
├── final_audio_ko/                  ← Stage 3: 생성된 개별 MP3 트랙 폴더
│   ├── final_track_00_intro.mp3
│   ├── final_track_01.mp3 ~ final_track_45.mp3
│   ├── closing.mp3
│   ├── part1_ko_list.txt ~ part6_ko_list.txt
│   └── merged/                      ← Stage 5: 최종 병합본 (6개 파트)
│       ├── blue_castle_ko_part1.mp3
│       └── ...
│
├── tag_dialogue_ko.py               ← 신규: Gemini 대화 태깅 도구
├── prepare_scripts_ko.py            ← 신규: JSON 대본 변환 도구
├── generate_audio_ko.py             ← 신규: edge-tts 오디오 합성 엔진
└── blue_castle_audio_roadmap.md     ← 이 문서
```

---

## 🏃 진행 현황 트래커 (Progress Tracker)

| 단계 | 작업 내용 | 상태 |
| :--- | :--- | :--- |
| **준비** | 한국어 챕터 번역 텍스트 확인 | ✅ 완료 |
| **Stage 1** | `tag_dialogue_ko.py` 작성 및 대화 태깅 진행 | ✅ 완료 |
| **Stage 2** | `prepare_scripts_ko.py` 작성 및 JSON 변환 완료 | ✅ 완료 |
| **Stage 3** | `generate_audio_ko.py` 작성 및 트랙 생성 | ✅ 완료 |
| **Stage 4** | 오디오 QA 청취 검수 | ✅ 완료 |
| **Stage 5** | ffmpeg concat 파트 병합 완료 | ✅ 완료 |
| **Stage 6** | 오디오북 최종 발행 | ⬜ 대기 (발행 준비 완료) |

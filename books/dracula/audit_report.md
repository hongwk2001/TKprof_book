# Dracula Bilingual Alignment Audit

## Audit 1: Paragraph & Word Count Summary

Verifies total paragraph counts and word counts for the raw English, chunked English, and final Korean files.

| Chapter | Raw EN (Para/Words) | Chunked EN (Para/Words) | Final KO (Para/Words) |
|---|---|---|---|
| 1 | 42 / 5,700 | 67 / 5,556 | 67 / 3,720 |
| 2 | 62 / 5,487 | 60 / 5,292 | 60 / 4,456 |
| 3 | 47 / 5,728 | 47 / 5,670 | 47 / 3,987 |
| 4 | 86 / 5,894 | 86 / 5,801 | 86 / 4,019 |
| 5 | 50 / 3,546 | 50 / 3,708 | 50 / 2,840 |
| 6 | 64 / 5,715 | 64 / 5,820 | 64 / 4,394 |
| 7 | 67 / 5,677 | 66 / 5,923 | 66 / 3,895 |
| 8 | 74 / 6,319 | 71 / 6,149 | 71 / 4,088 |
| 9 | 82 / 5,951 | 82 / 6,374 | 82 / 4,771 |
| 10 | 104 / 5,942 | 104 / 6,302 | 104 / 4,892 |
| 11 | 78 / 5,127 | 78 / 4,991 | 78 / 3,677 |
| 12 | 111 / 7,291 | 112 / 7,418 | 112 / 5,105 |
| 13 | 110 / 6,579 | 110 / 8,036 | 110 / 5,615 |
| 14 | 113 / 6,423 | 84 / 4,637 | 84 / 3,452 |
| 15 | 106 / 5,814 | 104 / 7,211 | 104 / 5,149 |
| 16 | 62 / 4,565 | 62 / 4,518 | 62 / 3,604 |
| 17 | 80 / 5,577 | 80 / 5,602 | 80 / 4,287 |
| 18 | 84 / 6,912 | 84 / 6,534 | 84 / 5,210 |
| 19 | 46 / 5,681 | 46 / 5,183 | 46 / 3,945 |
| 20 | 109 / 5,911 | 108 / 6,078 | 108 / 4,335 |
| 21 | 72 / 6,177 | 69 / 6,144 | 69 / 5,088 |
| 22 | 65 / 5,456 | 65 / 5,565 | 65 / 4,175 |
| 23 | 84 / 5,669 | 82 / 5,953 | 82 / 4,278 |
| 24 | 76 / 6,309 | 69 / 7,539 | 69 / 5,126 |
| 25 | 88 / 6,260 | 88 / 6,982 | 88 / 5,149 |
| 26 | 106 / 7,160 | 106 / 8,009 | 106 / 5,605 |
| 27 | 108 / 8,180 | 76 / 9,300 | 76 / 6,655 |
| **TOTAL** | **2176** | **2120** | **2120** |

---

## Audit 2: Per-Paragraph Misalignment Detection

Flags paragraphs where the Korean word count is **>4x the English word count** (for EN paragraphs ≥20 words).
A high ratio strongly suggests that the Korean paragraph contains content from a different section.

| Chapter | Para # | EN Words | KO Words | Ratio | Status |
|---|---|---|---|---|---|
| — | — | — | — | — | ✅ No issues found |
# Authors Republic & ACX Technical Requirements Reference Guide

This document summarizes the official technical specifications required by **Authors Republic** and major distributors (like ACX/Audible, Apple Books, and Spotify) for audiobook submissions.

---

## 1. Audio Specifications

Every audio file submitted must adhere strictly to the following parameters to pass automated quality control (QC):

| Metric | Requirement | Target / Optimal Value |
| :--- | :--- | :--- |
| **File Format** | MP3 (.mp3) | MP3 |
| **Bit Rate** | **192 kbps** or higher | **256 kbps** or **320 kbps** |
| **Bit Rate Mode** | **Constant Bit Rate (CBR)** (no VBR) | CBR |
| **Sample Rate** | Exactly **44.1 kHz** (44,100 Hz) | 44,100 Hz |
| **Channels** | Mono or Stereo (must match across all tracks) | Mono (recommended for standard audiobooks) |
| **Peak Amplitude** | Maximum **-3.0 dB** (no higher than -3.0 dB) | **-3.1 dB** to **-3.5 dB** (safeguard against clipping) |
| **RMS Volume** | Between **-23.0 dB RMS** and **-18.0 dB RMS** | **-20.0 dB RMS** |
| **Noise Floor** | Max **-60.0 dB RMS** (background room tone) | Below **-65.0 dB RMS** |
| **File Duration** | Maximum **120 minutes** (119 mins limit) | Split longer files into sub-parts |
| **File Size** | Maximum **170 MB** per file | Under 150 MB |

*   **Constant Bit Rate (CBR):** Constant Bit Rate is required (no VBR).
*   **Bitrate Consistency:** All files in the submission must match the exact same bitrate (e.g., all 192 kbps, or all 256 kbps). Mixing bitrates in the same project will cause automated/manual rejection.
*   **FFmpeg Implementation Warning (True Peak Margin of Error):** While ACX/AR requires a maximum of -3.0 dB True Peak, aiming for exactly -3.0 dB in an FFmpeg loudnorm filter can cause files to accidentally measure at -2.9 dB (a failure) during validation checks due to MP3 conversion artifacts on very long chapters. Always configure the True Peak target ceiling to **-3.2 dB to -3.5 dB** to guarantee a safe margin of error.
*   **The Linguistic LUFS Gap (Korean Edition Trap):** When mastering non-English TTS (particularly Korean language models), targeting -20.0 LUFS often results in a mathematical RMS that is too quiet (e.g. -23.5 dB to -24.4 dB). This is due to differences in phonetic spacing and dynamic speech range. For non-English texts, shift the FFmpeg target up to **-16.0 LUFS** to securely force the output RMS into the ACX compliant -18.0 to -23.0 dB window.

---

## 2. Silence & Padding Requirements

To ensure smooth transitions between chapters and tracks, specific silence boundaries must be built into each file:

*   **Leading Silence (Beginning):** Between **1.0 and 5.0 seconds** of clean silence (room tone only, no noise).
*   **Trailing Silence (Ending):** Between **1.0 and 5.0 seconds** of clean silence (room tone only, no noise).
*   *Note:* Ensure the silence contains a natural noise floor (room tone) rather than absolute digital silence (which sounds unnatural to listeners).
*   **The Short-Track RMS Trap:** Extremely short files (under 15 seconds, such as Opening or Closing tracks) will intrinsically fail the -23.0 dB RMS minimum if heavily padded, because silence mathematically drags the file's overall average down. 
    *   **The Fix:** For tracks under 15 seconds, reduce the silence padding to the absolute minimum allowed (**1.0 to 1.5 seconds**) and intentionally over-boost the target LUFS for the speech section (e.g. to **-16.0 LUFS** or **-10.0 LUFS**). This forcefully raises the file's overall mathematical RMS average into the safe -23 to -18 dB window without compromising the silence requirement.

---

## 3. Human QA Audit (Content Constraints)

In addition to the mathematical audio requirements, all audiobooks must pass strict human content audits:
1. **Dedicated Opening Credits:** The opening track MUST be a short, dedicated credits track that only reads the Title, Author, and Narrator (e.g., "[Title], by [Author]. Narrated by [Narrator]"). It MUST NOT contain the preface, introduction, or first chapter.
2. **No External Links:** The closing credits MUST NOT contain any URLs, website links, or external promotional material. It should simply conclude the audiobook (e.g., "The end." or "이상으로 [Title] 오디오북을 마칩니다.").

---

## 4. Required Tracks and Metadata

An audiobook submission must contain the following structural tracks:

1.  **Opening Credits:**
    *   **Strict Limit:** Opening track must include ONLY: **Title**, **Author**, and **Narrator**. Including excess info (copyrights, production credits) will cause rejection.
    *   **Example Script:** *"This is {Project Title}. Written by {Author Name(s)}. Narrated by {Narrator Name(s)}."*
2.  **Chapters/Sections:**
    *   Every chapter or main section must be a standalone file.
    *   Must announce the chapter number and title at the beginning of the file (e.g. *"Chapter 1: The Luxury Trap"*).
    *   **Silence Enforcement:** If no start-of-track silence is detected, the track will be rejected. Every track must contain **1 to 5 seconds of silence** at both the beginning and the end.
3.  **Closing Credits:**
    *   **Strict Rule:** Closing track must contain **ONLY** a concise ending statement.
    *   **Rejection Warning:** Including excess information (edition notes, review requests, word count comparisons, copyright boilerplate) in closing.mp3 will trigger immediate rejection.
4.  **Retail Sample:**
    *   Must be between **1 and 5 minutes** in duration.
    *   Must contain actual narration (not music or opening credits).

---

## 5. Cover Art Requirements

*   **Dimensions:** Exactly **2,400 x 2,400 pixels** (perfect square).
*   **Format:** JPEG (.jpg) or PNG (.png).
*   **Color Profile:** **RGB** color space (do NOT use CMYK print profiles).
*   **Exact Metadata Alignment:** Title, Subtitle, and Narrator must match exactly across metadata, cover art, and opening/closing tracks.
*   **Content Restrictions:** No promotional stickers, ratings, or references to physical formats (e.g., "CD", "includes PDF"). Cover image cannot be an image of a physical product (e.g., no 3D book cover templates).

---

## 6. Section Announcement & Front Matter Rules

*   **First Chapter Track (Preface/Intro/Chapter 1):** The first chapter track must begin with its own section announcement (e.g. *"Preface"* or *"Introduction"*) rather than repeating the book's main title/front matter. It should start directly with its section name.

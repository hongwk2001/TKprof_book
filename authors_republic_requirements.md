# 🎙️ Authors Republic & ACX Technical Requirements Reference Guide

This document summarizes the official technical specifications required by **Authors Republic** and major distributors (like ACX/Audible, Apple Books, and Spotify) for audiobook submissions.

---

## 🎧 1. Audio Specifications

Every audio file submitted must adhere strictly to the following parameters to pass automated quality control (QC):

| Metric | Requirement | Target / Optimal Value |
| :--- | :--- | :--- |
| **File Format** | MP3 (`.mp3`) | MP3 |
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

---

## ⏱️ 2. Silence & Padding Requirements

To ensure smooth transitions between chapters and tracks, specific silence boundaries must be built into each file:

*   **Leading Silence (Beginning):** Between **1.0 and 5.0 seconds** of clean silence (room tone only, no noise).
*   **Trailing Silence (Ending):** Between **1.0 and 5.0 seconds** of clean silence (room tone only, no noise).
*   *Note:* Ensure the silence contains a natural noise floor (room tone) rather than absolute digital silence (which sounds unnatural to listeners).

---

## 📂 3. Required Tracks and Metadata

An audiobook submission must contain the following structural tracks:

1.  **Opening Credits:**
    *   **Strict Limit:** Opening track must include ONLY: **Title**, **Author**, and **Narrator**. Including excess info (copyrights, production credits) will cause rejection.
    *   **Solution:** Move additional information into a separate chapter track (e.g., introduction or prologue).
    *   **Example Script:** *“This is {Project Title}. Written by {Author Name(s)}. Narrated by {Narrator Name(s)}.”*
2.  **Chapters/Sections:**
    *   Every chapter or main section must be a standalone file.
    *   Must announce the chapter number and title at the beginning of the file (e.g. *"Chapter 1: The Luxury Trap"*).
    *   **Silence Enforcement:** If no start-of-track silence is detected, the track will be rejected. Every track must contain **1 to 5 seconds of silence** at both the beginning and the end.
3.  **Closing Credits:**
    *   **Must include a reference to the book ending** (e.g. *"The End."* or *"You have been listening to..."*). This is required — tracks without an ending reference will be rejected.
    *   May also include title, author, narrator, and additional credits.
    *   **Example:** *"You have been listening to The Dog Crosses the Road. Written by John Doe, and read for you by Jane Doe. Published by Fantastic Publishing. Artwork by Fantastic Artwork."*
    *   Must announce the conclusion of the audiobook.
    *   Example script: *"This concludes the audiobook of [Title], written by [Author], narrated by [Narrator]. Copyright [Year] by [Publisher]."*
4.  **Retail Sample:**
    *   Must be between **1 and 5 minutes** in duration.
    *   Must contain actual narration (not music or opening credits).
    *   Must meet all standard quality checks (RMS, peak, sample rate).

---

## 🎨 4. Cover Art Requirements

Distributors display cover art at various sizes. To prevent rejection, graphics must meet these strict criteria:

*   **Dimensions:** Exactly **2,400 x 2,400 pixels** (perfect square).
*   **Format:** JPEG (`.jpg`) or PNG (`.png`).
*   **Resolution:** Minimum **72 dpi** (dots per inch).
*   **Color Profile:** **RGB** color space (do NOT use CMYK print profiles).
*   **File Size:** Under **5 MB**.
*   **Required Text:** Must match the metadata exactly (Title, Subtitle, and Author Name must match spelling in the audio credits).
*   **Exact Metadata Alignment:** 
    *   **Title** must match exactly across metadata, cover art, and opening/closing tracks.
    *   **Subtitle** must match exactly across metadata, cover art, and opening/closing tracks.
    *   **Narrator** must match exactly across metadata and opening/closing tracks.
*   **Content Restrictions:**
    *   No promotional stickers, ratings, or references to physical formats (e.g., "CD", "includes PDF").
    *   **Cover image cannot be an image of a physical product** (e.g., no 3D book cover templates, spines, CD mockups, or physical packaging). Cover art must be flat 2D artwork.
    *   Keep critical text away from the borders (especially the bottom-right corner, where player overlays often display play badges).

---

## 📖 5. Section Announcement & Front Matter Rules

To avoid confusing the listener or failing metadata checks:
*   **First Chapter Track (Preface/Intro/Chapter 1):** The first chapter track must begin with its own section announcement (e.g. *"Preface"* or *"Introduction"*) rather than repeating the book's main title/front matter (e.g. do not say *"The Science of Getting Rich: Modernized Edition. Preface."*). It should start directly with its section name.


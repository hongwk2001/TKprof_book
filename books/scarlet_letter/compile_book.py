"""
compile_book.py
Assembles all modernized chapter files for The Scarlet Letter into a single
compiled text file in the correct layout order:
  1. Introduction
  2. Chapters 1-24
  3. The Custom-House essay (ch_00)
  4. Copyright / Ending
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
OUTPUT_FILE = os.path.join(BASE_DIR, "scarlet_letter_compiled.txt")

SEPARATOR = "\n\n" + ("=" * 60) + "\n\n"


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def main():
    sections = []

    # 1. Introduction
    intro_path = os.path.join(BASE_DIR, "introduction_en.txt")
    sections.append(read_file(intro_path))
    print("Added: introduction_en.txt")

    # 2. Chapters 1-24
    for i in range(1, 25):
        filename = f"ch_{i:02d}_en.txt"
        path = os.path.join(CHAPTERS_DIR, filename)
        if os.path.exists(path):
            sections.append(read_file(path))
            print(f"Added: {filename}")
        else:
            print(f"WARNING: Missing {filename}")

    # 3. The Custom-House essay (placed at back)
    custom_house_path = os.path.join(CHAPTERS_DIR, "ch_00_en.txt")
    sections.append(read_file(custom_house_path))
    print("Added: ch_00_en.txt (The Custom-House)")

    # 4. Copyright / Ending
    copyright_path = os.path.join(BASE_DIR, "copyright_en.txt")
    sections.append(read_file(copyright_path))
    print("Added: copyright_en.txt")

    # Join all sections with separator
    compiled = SEPARATOR.join(sections)

    # Write output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(compiled)

    size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"\nCompilation complete.")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Size:   {size_kb:.1f} KB")
    print(f"Sections assembled: {len(sections)}")


if __name__ == "__main__":
    main()

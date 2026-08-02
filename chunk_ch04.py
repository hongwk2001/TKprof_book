import os

raw_file = r"d:\git_repo\TKprof_book\books\tono_bungay\chapters\book3\book3_ch04_en_raw.txt"
out_dir = r"d:\git_repo\TKprof_book\books\tono_bungay\chapters\book3\chunks"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

with open(raw_file, "r", encoding="utf-8") as f:
    text = f.read()

# We need to split into 23 chunks. Let's split by paragraphs first.
paragraphs = text.split("\n\n")

# Filter out empty paragraphs
paragraphs = [p.strip() for p in paragraphs if p.strip()]

num_chunks = 23
chunk_size = len(paragraphs) // num_chunks
remainder = len(paragraphs) % num_chunks

chunks = []
start = 0
for i in range(num_chunks):
    # distribute remainder across the first few chunks
    end = start + chunk_size + (1 if i < remainder else 0)
    chunks.append("\n\n".join(paragraphs[start:end]))
    start = end

for i, chunk_text in enumerate(chunks):
    # 0-indexed as 00, 01, etc.
    filename = os.path.join(out_dir, f"chunk_{i:02d}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(chunk_text)

print(f"Created {len(chunks)} chunks.")

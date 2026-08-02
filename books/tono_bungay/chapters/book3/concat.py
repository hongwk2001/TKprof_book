import os

chunk_dir = r"d:\git_repo\TKprof_book\books\tono_bungay\chapters\book3\chunks"
ko_out = r"d:\git_repo\TKprof_book\books\tono_bungay\chapters\book3\book3_ch01_ko.txt"
en_out = r"d:\git_repo\TKprof_book\books\tono_bungay\chapters\book3\book3_ch01_en.txt"

def concat_files(prefix, out_path, num_chunks=5):
    with open(out_path, 'w', encoding='utf-8') as out_f:
        for i in range(1, num_chunks + 1):
            chunk_file = os.path.join(chunk_dir, f"{prefix}_chunk_{i}.txt")
            if os.path.exists(chunk_file):
                with open(chunk_file, 'r', encoding='utf-8') as in_f:
                    out_f.write(in_f.read())
                    out_f.write("\n")

concat_files("ko", ko_out)
concat_files("en", en_out)
print("Concatenation complete.")

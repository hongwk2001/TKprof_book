import os
import sys
import re
import json

BASE_DIR = r"d:\git_repo\TKprof_book\books\odyssey"
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
TEMP_DIR = os.path.join(BASE_DIR, "temp_chunks")

def split_into_paragraphs(text):
    paras = re.split(r'\n\s*\n', text)
    return [p.strip() for p in paras if p.strip()]

def split_chapter(ch_num, batch_size=10):
    os.makedirs(TEMP_DIR, exist_ok=True)
    src_filename = f"ch_{ch_num:02d}_en.txt"
    src_path = os.path.join(CHAPTERS_DIR, src_filename)
    
    if not os.path.exists(src_path):
        print(f"Error: Source chapter {src_path} not found.")
        return False
        
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    paragraphs = split_into_paragraphs(content)
    total_batches = (len(paragraphs) + batch_size - 1) // batch_size
    print(f"Splitting Chapter {ch_num} ({len(paragraphs)} paragraphs) into {total_batches} chunks...")
    
    for idx in range(total_batches):
        batch = paragraphs[idx*batch_size : (idx+1)*batch_size]
        chunk_text = "\n\n".join(batch)
        chunk_filename = f"ch_{ch_num:02d}_en_chunk_{idx:02d}.txt"
        chunk_path = os.path.join(TEMP_DIR, chunk_filename)
        with open(chunk_path, "w", encoding="utf-8") as f_out:
            f_out.write(chunk_text)
            
    # Save a metadata file for progress tracking
    meta_path = os.path.join(TEMP_DIR, f"ch_{ch_num:02d}_meta.json")
    meta = {
        "chapter": ch_num,
        "total_chunks": total_batches,
        "batch_size": batch_size,
        "total_paragraphs": len(paragraphs)
    }
    with open(meta_path, "w", encoding="utf-8") as f_meta:
        json.dump(meta, f_meta, indent=2)
        
    return True

def merge_chapter(ch_num):
    meta_path = os.path.join(TEMP_DIR, f"ch_{ch_num:02d}_meta.json")
    if not os.path.exists(meta_path):
        print(f"Error: Metadata not found for Chapter {ch_num}.")
        return False
        
    with open(meta_path, "r", encoding="utf-8") as f_meta:
        meta = json.load(f_meta)
        
    total_chunks = meta["total_chunks"]
    dest_filename = f"ch_{ch_num:02d}_ko.txt"
    dest_path = os.path.join(CHAPTERS_DIR, dest_filename)
    
    chunks_content = []
    for idx in range(total_chunks):
        ko_chunk_filename = f"ch_{ch_num:02d}_ko_chunk_{idx:02d}.txt"
        ko_chunk_path = os.path.join(TEMP_DIR, ko_chunk_filename)
        
        if not os.path.exists(ko_chunk_path):
            print(f"Error: Missing Korean chunk {ko_chunk_filename} for Chapter {ch_num}.")
            return False
            
        with open(ko_chunk_path, "r", encoding="utf-8") as f_chunk:
            chunks_content.append(f_chunk.read().strip())
            
    # Write merged file
    with open(dest_path, "w", encoding="utf-8") as f_out:
        f_out.write("\n\n".join(chunks_content))
        
    print(f"Chapter {ch_num} successfully merged into {dest_filename}.")
    
    # Cleanup temp files for this chapter
    for idx in range(total_chunks):
        try:
            os.remove(os.path.join(TEMP_DIR, f"ch_{ch_num:02d}_en_chunk_{idx:02d}.txt"))
            os.remove(os.path.join(TEMP_DIR, f"ch_{ch_num:02d}_ko_chunk_{idx:02d}.txt"))
        except OSError:
            pass
    try:
        os.remove(meta_path)
    except OSError:
        pass
        
    return True

def status():
    if not os.path.exists(TEMP_DIR):
        print("No active chunks.")
        return
        
    files = os.listdir(TEMP_DIR)
    meta_files = [f for f in files if f.endswith("_meta.json")]
    if not meta_files:
        print("No active chapters in translation.")
        return
        
    print("Translation Status:")
    for meta_file in sorted(meta_files):
        with open(os.path.join(TEMP_DIR, meta_file), "r", encoding="utf-8") as f:
            meta = json.load(f)
        ch = meta["chapter"]
        total = meta["total_chunks"]
        done = 0
        pending = []
        for idx in range(total):
            ko_chunk = f"ch_{ch:02d}_ko_chunk_{idx:02d}.txt"
            if os.path.exists(os.path.join(TEMP_DIR, ko_chunk)):
                done += 1
            else:
                pending.append(idx)
        print(f"  Chapter {ch:02d}: {done}/{total} chunks translated. Pending: {pending}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python translate_helper.py [split|merge|status] [ch_num]")
        sys.exit(1)
        
    cmd = sys.argv[1]
    if cmd == "split":
        ch_num = int(sys.argv[2])
        split_chapter(ch_num)
    elif cmd == "merge":
        ch_num = int(sys.argv[2])
        merge_chapter(ch_num)
    elif cmd == "status":
        status()
    else:
        print(f"Unknown command: {cmd}")

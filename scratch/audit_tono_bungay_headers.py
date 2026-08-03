import os
import glob

def audit_headers():
    base_dir = r"c:\git_repo\TKprof_book\books\tono_bungay\chapters"
    output_lines = []
    
    for book_num in range(1, 5):
        book_dir = os.path.join(base_dir, f"book{book_num}")
        if not os.path.exists(book_dir):
            continue
            
        files = glob.glob(os.path.join(book_dir, "*.txt"))
        files = [f for f in files if f.endswith("_en.txt") or f.endswith("_ko.txt")]
        files.sort()
        
        for file in files:
            output_lines.append(f"--- {os.path.basename(file)} ---")
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                non_empty = [l.strip() for l in lines if l.strip()]
                for i in range(min(5, len(non_empty))):
                    output_lines.append(f"{i+1}: {non_empty[i]}")
            output_lines.append("")
            
    with open(r"c:\git_repo\TKprof_book\scratch\tono_bungay_headers_audit.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

if __name__ == "__main__":
    audit_headers()

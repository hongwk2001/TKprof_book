import subprocess
import time
import sys

def main():
    chapters = list(range(3, 28)) # Chapters 3 to 27
    batch_size = 5
    book = "secret_garden"
    
    print(f"Starting parallel modernization for chapters: {chapters}")
    
    # Process in batches of 5
    for i in range(0, len(chapters), batch_size):
        batch = chapters[i:i+batch_size]
        print(f"\n--- Spawning batch: {batch} ---")
        processes = []
        for ch in batch:
            cmd = ["python", "books/modernize_book.py", "--book", book, "--chapters", str(ch)]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            processes.append((ch, p))
            print(f"Spawned Chapter {ch}")
            
        # Wait for all processes in the current batch to finish
        for ch, p in processes:
            stdout, stderr = p.communicate()
            if p.returncode == 0:
                print(f"Chapter {ch} completed successfully.")
            elif p.returncode == 2:
                print(f"[QUOTA_EXHAUSTED] Chapter {ch} hit quota limits. Exiting.")
                sys.exit(2)
            else:
                print(f"Chapter {ch} failed with return code {p.returncode}")
                print(f"Stderr: {stderr}")
                
        print(f"Completed batch: {batch}")
        # Add a brief pause between batches to respect rate limits
        print("Waiting 10 seconds before next batch...")
        time.sleep(10)

if __name__ == "__main__":
    main()

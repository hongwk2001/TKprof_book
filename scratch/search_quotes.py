import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIRS = [
    os.path.join(BASE_DIR, "books", "secret_garden", "chapters", "tagged"),
    os.path.join(BASE_DIR, "books", "secret_garden", "scripts_en"),
    os.path.join(BASE_DIR, "books", "secret_garden", "scripts_ko")
]

def search_escaped_quotes(directory):
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return 0
        
    print(f"\nScanning: {os.path.relpath(directory, BASE_DIR)}...")
    occurrences = 0
    
    files = sorted([f for f in os.listdir(directory) if f.endswith(".txt") or f.endswith(".json")])
    for filename in files:
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines):
                # Search for literal \\\" inside the string representation
                if '\\"' in line:
                    print(f"  {filename}:{i+1} -> {line.strip()}")
                    occurrences += 1
        except Exception as e:
            print(f"  Error reading {filename}: {e}")
            
    return occurrences

def main():
    total_found = 0
    for directory in TARGET_DIRS:
        total_found += search_escaped_quotes(directory)
        
    print("\n" + "="*60)
    print(f"Search complete. Found {total_found} occurrences of escaped quotes (\\\")")
    print("="*60)

if __name__ == "__main__":
    main()

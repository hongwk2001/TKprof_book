import os

def main():
    filepath = 'books/dracula/chapters_backup/raw_ch_21.txt'
    
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')
        
    # Let's perform the splits
    # Split 1: R045 (moonlight scene)
    # Target 1: even to the scar on his forehead. With his left
    target1 = 'even to the scar on his forehead. With his left'
    replacement1 = 'even to the scar on his forehead.\n\nWith his left'
    
    if target1 in content:
        content = content.replace(target1, replacement1)
        print("Split 1 applied (R045 Part A/B)")
    else:
        print("Warning: target1 not found in raw_ch_21.txt")
        
    # Target 2: and sprang at us. But by this time the Professor
    target2 = 'and sprang at us. But by this time the Professor'
    replacement2 = 'and sprang at us.\n\nBut by this time the Professor'
    
    if target2 in content:
        content = content.replace(target2, replacement2)
        print("Split 2 applied (R045 Part B/C)")
    else:
        print("Warning: target2 not found in raw_ch_21.txt")
        
    # Split 2: R066 (Dracula speech scene)
    # Target 3: do my bidding; and to that end this!’ With that he pulled
    target3 = 'do my bidding; and to that end this!’ With that he pulled'
    replacement3 = 'do my bidding; and to that end this!’\n\nWith that he pulled'
    
    # Also handle alternate quote character if present
    target3_alt = 'do my bidding; and to that end this!" With that he pulled'
    replacement3_alt = 'do my bidding; and to that end this!"\n\nWith that he pulled'
    
    if target3 in content:
        content = content.replace(target3, replacement3)
        print("Split 3 applied (R066 Speech/Assault)")
    elif target3_alt in content:
        content = content.replace(target3_alt, replacement3_alt)
        print("Split 3 applied (R066 Speech/Assault alt quote)")
    else:
        print("Warning: target3 not found in raw_ch_21.txt")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Successfully updated raw text in backup directory: {filepath}")

if __name__ == '__main__':
    main()

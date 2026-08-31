import re

def clean_tag(text):
    return re.sub(r'^\[P[0-9a-zA-Z_]+\]\s*', '', text.strip())

def main():
    en_path = 'books/dracula/chapters/ch21_en.txt'
    ko_path = 'books/dracula/chapters/ch21_ko.txt'
    
    with open(en_path, 'r', encoding='utf-8') as f:
        en_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
        
    with open(ko_path, 'r', encoding='utf-8') as f:
        ko_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
        
    target_tags = ['[P036]', '[P045]', '[P062_063]', '[P066]']
    
    md_lines = [
        "# Proposed Paragraph Splits for Chapter 21",
        "",
        "This document details the exact proposed splits for the four long paragraphs in Chapter 21.",
        ""
    ]
    
    for tag in target_tags:
        en_p = next((p for p in en_paras if p.startswith(tag)), None)
        ko_p = next((p for p in ko_paras if p.startswith(tag)), None)
        
        if not en_p or not ko_p:
            continue
            
        md_lines.append(f"## Paragraph {tag}")
        md_lines.append("")
        md_lines.append("### English original")
        md_lines.append(f"> {clean_tag(en_p)}")
        md_lines.append("")
        md_lines.append("### Korean original")
        md_lines.append(f"> {clean_tag(ko_p)}")
        md_lines.append("")
        
        # Proposed splits
        en_clean = clean_tag(en_p)
        ko_clean = clean_tag(ko_p)
        
        md_lines.append("### Proposed Split Plan")
        md_lines.append("")
        
        if tag == '[P036]':
            # This is a merge of R036 and R037
            # In English, split at: "I saw a red cloud, heard a sound like thunder, and then the mist seemed to slip away under the door." His voice was...
            # and next part starts with "Now we know the worst"
            en_split1 = en_clean.split('His voice was growing fainter, and his breathing was getting worse. Van Helsing stood up instinctively.')[0].strip() + ' His voice was growing fainter, and his breathing was getting worse. Van Helsing stood up instinctively.'
            en_split2 = en_clean.split('His voice was growing fainter, and his breathing was getting worse. Van Helsing stood up instinctively.')[1].strip()
            
            # In Korean, we need to find the equivalent split point.
            # Let's search for keywords in Korean:
            # "그의 목소리는 점점 더 희미해졌고..."
            # Let's do a regex split or substring find in Korean.
            ko_split_marker = "그의 목소리는 점점 더 가늘어졌고, 숨소리도 더욱 가빠졌다. 반 헬싱 교수님은 본능적으로 일어서셨다."
            if ko_split_marker in ko_clean:
                ko_split1 = ko_clean.split(ko_split_marker)[0].strip() + " " + ko_split_marker
                ko_split2 = ko_clean.split(ko_split_marker)[1].strip()
            else:
                ko_split1 = ko_clean[:len(ko_clean)//2]
                ko_split2 = ko_clean[len(ko_clean)//2:]
                
            md_lines.append("| Tag | English Text | Korean Text |")
            md_lines.append("|---|---|---|")
            md_lines.append(f"| **`[P036]`** | {en_split1[:150]}... | {ko_split1[:150]}... |")
            md_lines.append(f"| **`[P037]`** | {en_split2[:150]}... | {ko_split2[:150]}... |")
            
        elif tag == '[P045]':
            # Split into 3 parts:
            # Part 1 ends at: "scar on his forehead."
            # Part 2 ends at: "lunged at us."
            # Part 3 starts with: "But by that time..."
            
            en_split1 = en_clean.split('scar on his forehead.')[0].strip() + ' scar on his forehead.'
            en_rest = en_clean.split('scar on his forehead.')[1].strip()
            en_split2 = en_rest.split('lunged at us.')[0].strip() + ' lunged at us.'
            en_split3 = en_rest.split('lunged at us.')[1].strip()
            
            # Korean equivalent split markers:
            # Marker 1: "이마의 흉터까지 틀림없는 백작의 모습이었다."
            # Marker 2: "우리에게 달려들었다."
            ko_marker1 = "이마의 흉터까지 틀림없는 백작의 모습이었다."
            ko_marker2 = "우리에게 달려들었다."
            
            if ko_marker1 in ko_clean and ko_marker2 in ko_clean:
                ko_split1 = ko_clean.split(ko_marker1)[0].strip() + " " + ko_marker1
                ko_rest = ko_clean.split(ko_marker1)[1].strip()
                ko_split2 = ko_rest.split(ko_marker2)[0].strip() + " " + ko_marker2
                ko_split3 = ko_rest.split(ko_marker2)[1].strip()
            else:
                ko_split1 = ko_clean[:len(ko_clean)//3]
                ko_split2 = ko_clean[len(ko_clean)//3: 2*len(ko_clean)//3]
                ko_split3 = ko_clean[2*len(ko_clean)//3:]
                
            md_lines.append("| Tag | English Text | Korean Text |")
            md_lines.append("|---|---|---|")
            md_lines.append(f"| **`[P045a]`** | {en_split1[:150]}... | {ko_split1[:150]}... |")
            md_lines.append(f"| **`[P045b]`** | {en_split2[:150]}... | {ko_split2[:150]}... |")
            md_lines.append(f"| **`[P045c]`** | {en_split3[:150]}... | {ko_split3[:150]}... |")
            
        elif tag == '[P062_063]':
            # Split into R062 and R063
            # English ends at: "organize her thoughts, she began:"
            en_split1 = en_clean.split('organize her thoughts, she began:')[0].strip() + ' organize her thoughts, she began:'
            en_split2 = en_clean.split('organize her thoughts, she began:')[1].strip()
            
            # Korean equivalent marker:
            # "마침내 생각을 정리할 시간이 조금 필요했던 것인지, 짧은 침묵을 거친 후에 미나 부인이 입을 열었다."
            ko_marker = "짧은 침묵을 거친 후에 미나 부인이 입을 열었다."
            if ko_marker in ko_clean:
                ko_split1 = ko_clean.split(ko_marker)[0].strip() + " " + ko_marker
                ko_split2 = ko_clean.split(ko_marker)[1].strip()
            else:
                ko_split1 = ko_clean[:len(ko_clean)//2]
                ko_split2 = ko_clean[len(ko_clean)//2:]
                
            md_lines.append("| Tag | English Text | Korean Text |")
            md_lines.append("|---|---|---|")
            md_lines.append(f"| **`[P062]`** | {en_split1[:150]}... | {ko_split1[:150]}... |")
            md_lines.append(f"| **`[P063]`** | {en_split2[:150]}... | {ko_split2[:150]}... |")
            
        elif tag == '[P066]':
            # Split into Dracula's speech and the forced blood-drinking assault
            # English split at: "And this is how we ensure that!'"
            en_split1 = en_clean.split("And this is how we ensure that!'")[0].strip() + " And this is how we ensure that!'"
            en_split2 = en_clean.split("And this is how we ensure that!'")[1].strip()
            
            # Korean equivalent split marker:
            # "이것이 바로 내가 그것을 보장하는 방법이다!'"
            ko_marker = "이것이 바로 내가 그것을 보장하는 방법이다!'"
            if ko_marker in ko_clean:
                ko_split1 = ko_clean.split(ko_marker)[0].strip() + " " + ko_marker
                ko_split2 = ko_clean.split(ko_marker)[1].strip()
            else:
                ko_split1 = ko_clean[:len(ko_clean)//2]
                ko_split2 = ko_clean[len(ko_clean)//2:]
                
            md_lines.append("| Tag | English Text | Korean Text |")
            md_lines.append("|---|---|---|")
            md_lines.append(f"| **`[P066a]`** | {en_split1[:150]}... | {ko_split1[:150]}... |")
            md_lines.append(f"| **`[P066b]`** | {en_split2[:150]}... | {ko_split2[:150]}... |")
            
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        
    artifact_path = r'C:\Users\hongw\.gemini\antigravity\brain\3ddf8683-f4e2-437b-8ee1-79e2d403a4a0\proposed_splits.md'
    with open(artifact_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
        
    print(f"Proposed splits written to {artifact_path}")

if __name__ == '__main__':
    main()

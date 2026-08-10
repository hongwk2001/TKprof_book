import os
import re

def split_into_sentences(text):
    # Split text into sentences.
    # We want to split after sentence-ending punctuation, optionally followed by quotes, then space.
    # Since regex can be tricky, let's just split by punctuation and re-attach it.
    
    # A simpler approach: find all occurrences of punctuation+quotes, and add a special token
    # to split on.
    text = text.replace('\n', ' ')
    text = re.sub(r'([.?!][\'\"]?)\s+', r'\1<SPLIT>', text)
    sentences = text.split('<SPLIT>')
    return [s.strip() for s in sentences if s.strip()]

def align_chapter(ch_num):
    ch = f"ch{ch_num:02d}"
    en_file = f"books/dracula/chapters/{ch}_en.txt"
    ko_file = f"books/dracula/chapters/{ch}_ko.txt"
    
    if not os.path.exists(en_file) or not os.path.exists(ko_file):
        return
        
    with open(en_file, 'r', encoding='utf-8', errors='replace') as f:
        en_paras = [p for p in f.read().split('\n\n') if p.strip()]
        
    with open(ko_file, 'r', encoding='utf-8', errors='replace') as f:
        ko_text = f.read()
        ko_paras_orig = [p for p in ko_text.split('\n\n') if p.strip()]
        
    if len(en_paras) == len(ko_paras_orig):
        print(f"{ch}: Paragraph counts match ({len(en_paras)}).")
        return
        
    print(f"{ch}: Aligning {len(ko_paras_orig)} KO paras to {len(en_paras)} EN paras...")
    
    ko_sentences = split_into_sentences(ko_text)
    
    total_en_len = sum(len(p) for p in en_paras)
    total_ko_len = sum(len(s) for s in ko_sentences)
    
    if total_en_len == 0 or total_ko_len == 0:
        return
        
    ratio = total_ko_len / total_en_len
    
    new_ko_paras = [''] * len(en_paras)
    
    if len(ko_sentences) < len(en_paras):
        # We don't have enough sentences. Just distribute what we have and pad with empty strings.
        for i in range(len(ko_sentences)):
            new_ko_paras[i] = ko_sentences[i]
    else:
        # We have enough sentences. Assign them based on target length, ensuring at least one per para.
        sentence_idx = 0
        for i, en_p in enumerate(en_paras):
            # Calculate how many sentences are left and how many paragraphs are left
            paras_left = len(en_paras) - i
            sentences_left = len(ko_sentences) - sentence_idx
            
            if paras_left == 1:
                # Last paragraph gets all remaining sentences
                new_ko_paras[i] = ' '.join(ko_sentences[sentence_idx:])
                break
                
            # Must leave at least paras_left - 1 sentences for the remaining paragraphs
            max_sentences = sentences_left - (paras_left - 1)
            
            target_ko_len = len(en_p) * ratio
            accumulated_len = 0
            current_ko_para_sentences = []
            
            while sentence_idx < len(ko_sentences) and len(current_ko_para_sentences) < max_sentences:
                sent = ko_sentences[sentence_idx]
                current_ko_para_sentences.append(sent)
                accumulated_len += len(sent)
                sentence_idx += 1
                
                # We stop if we hit target length, AND we have at least 1 sentence
                if accumulated_len >= target_ko_len and len(current_ko_para_sentences) >= 1:
                    break
                    
            if not current_ko_para_sentences and sentence_idx < len(ko_sentences):
                current_ko_para_sentences.append(ko_sentences[sentence_idx])
                sentence_idx += 1
                
            new_ko_paras[i] = ' '.join(current_ko_para_sentences)
        
    # Write back
    with open(ko_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(new_ko_paras))
    print(f"{ch}: Alignment complete.")

for i in range(1, 28):
    align_chapter(i)

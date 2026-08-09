import re

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\raw_ch_27.txt', 'r', encoding='utf-8') as f:
    text = f.read()

paras = text.split('\n\n')

splits = {
    2: [
        r"The horses seem to know that they are being kindly treated",
        r"We have now had so many changes and find the same thing",
        r"We are travelling fast, and as we have no driver",
        r"All is ready; we are off shortly\."
    ],
    4: [
        r"There is a strange heaviness in the air",
        r"It is very cold, and only our warm furs",
        r"At dawn Van Helsing hypnotised me;"
    ],
    6: [
        r"We both seem in good spirits;",
        r"The houses are very few here now",
        r"The dear horses are patient and good",
        r"We shall get to the Pass in daylight;",
        r"Oh, what will to-morrow bring to us\?",
        r"God grant that we may be guided aright",
        r"Alas!"
    ],
    8: [
        r"It is cold, cold; so cold",
        r"It seems to have affected Madam Mina;",
        r"However, to-night she is more _vif_\.",
        r"Well, God’s will be done"
    ],
    10: [
        r"When I saw the signs of the dawn",
        r"We stopped our carriage, and got down",
        r"I made a couch with furs,"
    ],
    15: [
        r"Then we go on for long, long hours",
        r"But she sleep on, and I may not wake her",
        r"I think I drowse myself, for all of sudden",
        r"I look down and find Madam Mina still sleep\.",
        r"It is now not far off sunset time,"
    ],
    16: [
        r"I am amaze, and not at ease then;"
    ]
}

split_count = 0

for i, p in enumerate(paras):
    if i in splits:
        for target in splits[i]:
            # Convert target spaces to allow for newlines
            pattern = target.replace(' ', r'\s+')
            match = re.search(pattern, p)
            if match:
                idx = match.start()
                # Insert \n\n before the target, but we should remove the trailing space before the target if it exists,
                # wait, the instruction says "only insert paragraph breaks (\n\n)", so we should just insert it!
                # Actually, replacing the space with \n\n is exactly what "inserting paragraph breaks" means for natural text formatting.
                # If we keep the space, we get `\n\n The horses...` which is weird. 
                # Let's replace the preceding space/newline with `\n\n`.
                
                # Let's find the space before the match
                before = p[:idx]
                after = p[idx:]
                if before and re.match(r'\s', before[-1]):
                    p = before[:-1] + '\n\n' + after
                else:
                    p = before + '\n\n' + after
                split_count += 1
            else:
                print(f"Target not found: {target}")
        paras[i] = p

print(f"Total splits performed: {split_count}")

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\aligned_en_ch27.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(paras))

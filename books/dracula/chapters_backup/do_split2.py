import re

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\raw_ch_27.txt', 'r', encoding='utf-8') as f:
    text = f.read()

paras = text.split('\n\n')

splits = {
    2: [
        "The horses seem to know that they are being kindly treated",
        "We have now had so many changes and find the same thing",
        "We are travelling fast, and as we have no driver",
        "All is ready; we are off shortly."
    ],
    4: [
        "There is a strange heaviness in the air",
        "It is very cold, and only our warm furs",
        "At dawn Van Helsing hypnotised me;"
    ],
    6: [
        "We both seem in good spirits;",
        "The houses are very few here now",
        "The dear horses are patient and good",
        "We shall get to the Pass in daylight;",
        "Oh, what will to-morrow bring to us?",
        "God grant that we may be guided aright",
        "Alas!"
    ],
    8: [
        "It is cold, cold; so cold",
        "It seems to have affected Madam Mina;",
        "However, to-night she is more _vif_.",
        "Well, God’s will be done"
    ],
    10: [
        "When I saw the signs of the dawn",
        "We stopped our carriage, and got down",
        "I made a couch with furs,"
    ],
    15: [
        "Then we go on for long, long hours",
        "But she sleep on, and I may not wake her",
        "I think I drowse myself, for all of sudden",
        "I look down and find Madam Mina still sleep.",
        "It is now not far off sunset time,"
    ],
    16: [
        "I am amaze, and not at ease then;"
    ]
}

split_count = 0

for i, p in enumerate(paras):
    if i in splits:
        for target in splits[i]:
            # Find the target in the paragraph
            idx = p.find(target)
            if idx != -1:
                # Insert \n\n before the target, removing the space before it
                # Wait, there might be a space or newline before it
                before_idx = idx - 1
                while before_idx >= 0 and p[before_idx] in [' ', '\n']:
                    before_idx -= 1
                
                # We should replace the space/newline with \n\n?
                # The prompt says "only insert paragraph breaks (\n\n)". 
                # If we replace a space with \n\n, we are deleting a space.
                # If we just insert \n\n before the target, it's safer.
                p = p[:idx] + '\n\n' + p[idx:]
                split_count += 1
            else:
                print(f"Target not found: {target}")
        paras[i] = p

print(f"Total splits performed: {split_count}")

# wait, we just want to output the whole text joined by \n\n
with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\aligned_en_ch27.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(paras))

import json

voices = {
    'Lotty': {'voice': 'ko-KR-SunHiNeural', 'speed': 1.05},
    'Rose': {'voice': 'ko-KR-SunHiNeural', 'speed': 0.95},
    'Other': {'voice': 'ko-KR-HyunsuMultilingualNeural', 'speed': 1.0}
}
def get_chunk(ch, index, new_char):
    with open(f'd:/git_repo/TKprof_book/books/the_enchanted_april/scripts_ko/script_ch_{ch}.json', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(f'd:/git_repo/TKprof_book/books/the_enchanted_april/scripts_ko/script_ch_{ch}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    obj = data[index]
    old_char = obj['character']
    old_voice = obj['voice']
    old_speed = obj['speed']
    text_start = obj['text'].split('\n')[0][:15]
    start_idx = -1
    for i, line in enumerate(lines):
        if '"text":' in line and text_start in line:
            if f'"character": "{old_char}"' in lines[i-3]:
                start_idx = i - 3
                break
    if start_idx == -1:
        print('ERROR', ch, index)
        return
    target = "".join(lines[start_idx:start_idx+3])
    rep = target.replace(f'"character": "{old_char}"', f'"character": "{new_char}"')
    rep = rep.replace(f'"voice": "{old_voice}"', f'"voice": "{voices[new_char]["voice"]}"')
    rep = rep.replace(f'"speed": {old_speed}', f'"speed": {voices[new_char]["speed"]}')
    print(f"{{ 'StartLine': {start_idx+1}, 'EndLine': {start_idx+3}, 'TargetContent': {repr(target)}, 'ReplacementContent': {repr(rep)}, 'AllowMultiple': False }},")

changes = {
    17: [(22, 'Other'), (33, 'Other'), (86, 'Rose'), (88, 'Rose'), (91, 'Rose'), (93, 'Rose'), (95, 'Rose')]
}
for ch, idxs in changes.items():
    print(f'File: script_ch_{ch}.json')
    for idx, char in idxs:
        get_chunk(ch, idx, char)

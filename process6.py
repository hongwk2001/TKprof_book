import json
chapter_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_20.json'
queue_path = 'c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json'

updates = {
    "P024_2": {"ko": "감사합니다, Darnay.", "en": "I thank you, Darnay."},
    "P024_3": {"ko": "당신의 이름을 그렇게 편하게 불러도 되겠습니까?”", "en": "May I use that freedom with your name?”"},
    "P025_1": {"ko": "“이제는 그래도 될 때가 된 것 같군요, Carton.”", "en": "“I think so, Carton, by this time.”"},
    "P026_1": {"ko": "그들은 그 말에 악수를 나누었고, Sydney는 돌아섰다.", "en": "They shook hands upon it, and Sydney turned away."},
    "P026_2": {"ko": "1분도 채 지나지 않아, 그는 겉보기에는 전과 다름없이 헛된 모습으로 돌아갔다.", "en": "Within a minute afterward, he was, to all outward appearance, as insubstantial as ever."},
    "P027_1": {"ko": "그가 돌아간 후, Miss Pross, 박사님, 그리고 Mr.", "en": "When he was gone, and in the course of an evening passed with Miss Pross, the Doctor, and Mr."},
    "P027_2": {"ko": "Lorry와 함께 저녁 시간을 보내는 동안, Charles Darnay는 이 대화에 대해 대략적으로 언급하며 Sydney Carton을 부주의하고 무모한 골칫거리로 이야기했다.", "en": "Lorry, Charles Darnay made some mention of this conversation in general terms and spoke of Sydney Carton as a problem of carelessness and recklessness."},
    "P027_3": {"ko": "요컨대 그는 Carton을 비난하거나 가혹하게 대할 의도로 그렇게 말한 것이 아니라, 그가 보여주는 모습 그대로를 본 사람이라면 누구나 할 법한 그런 말투로 이야기했다.", "en": "He spoke of him, in short, not bitterly or meaning to bear hard upon him, but as anyone might who saw him as he showed himself."},
    "P028_1": {"ko": "그는 이 이야기가 그의 아름답고 어린 아내의 마음속에 남으리라고는 전혀 생각지 못했다;", "en": "He had no idea that this could dwell in the thoughts of his fair young wife;"},
    "P028_2": {"ko": "하지만 나중에 부부의 방으로 돌아왔을 때, 그는 특유의 그 예쁜 이마를 찌푸린 채 깊은 생각에 잠겨 자신을 기다리고 있는 그녀를 발견했다.", "en": "but when he later joined her in their own rooms, he found her waiting for him, with the old pretty lifting of the forehead strongly marked."}
}

with open(chapter_path, 'r', encoding='utf-8') as f:
    chapter = json.load(f)
for item in chapter:
    if item.get('tag') in updates:
        item['ko'] = updates[item['tag']]['ko']
        item['en'] = updates[item['tag']]['en']
with open(chapter_path, 'w', encoding='utf-8') as f:
    json.dump(chapter, f, indent=2, ensure_ascii=False)

with open(queue_path, 'r', encoding='utf-8') as f:
    queue = json.load(f)
for batch in queue:
    if batch['batch_id'] == 'book2_ch_20.json__batch0006':
        batch['status'] = 'done'
with open(queue_path, 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)
print("Done batch 6")

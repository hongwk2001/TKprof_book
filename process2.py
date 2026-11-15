import json
chapter_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_20.json'
queue_path = 'c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json'

updates = {
    "P010_4": {"ko": "놀라지 마십시오;", "en": "Don't be alarmed;"},
    "P010_5": {"ko": "설교를 늘어놓으려는 것은 아니니까요.”", "en": "I am not going to preach.”"},
    "P011_1": {"ko": "“전혀 놀라지 않았습니다.", "en": "“I am not at all alarmed."},
    "P011_2": {"ko": "당신의 진지한 모습은 제게 전혀 놀랍지 않습니다.”", "en": "Earnestness in you is anything but alarming to me.”"},
    "P012_1": {"ko": "“아!” Carton이 마치 그 말을 흘려보내려는 듯 손을 무심하게 저으며 말했다. “문제의 그 취했던 날 (당신도 아시다시피 수많은 그런 날들 중 하나였죠), 제가 당신을 좋아하는지 안 좋아하는지 참을 수 없을 정도로 떠들어댔었죠.", "en": "“Ah!” said Carton, with a careless wave of his hand, as if he waved that away. “On the drunken occasion in question (one of a large number, as you know), I was insufferable about liking you and not liking you."},
    "P012_2": {"ko": "그 일은 잊어주셨으면 합니다.”", "en": "I wish you would forget it.”"},
    "P013_1": {"ko": "“이미 오래전에 잊었습니다.”", "en": "“I forgot it long ago.”"},
    "P014_1": {"ko": "“또 의례적인 인사말이군요!", "en": "“Figure of speech again!"},
    "P014_2": {"ko": "하지만 Mr.", "en": "But Mr."},
    "P014_3": {"ko": "Darnay, 당신이 말하는 것처럼 제게 잊는다는 것은 그리 쉬운 일이 아닙니다.", "en": "Darnay, oblivion is not as easy for me as you represent it to be for you."}
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
    if batch['batch_id'] == 'book2_ch_20.json__batch0002':
        batch['status'] = 'done'
with open(queue_path, 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)
print("Done batch 2")

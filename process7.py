import json
chapter_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_20.json'
queue_path = 'c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json'

updates = {
    "P029_1": {"ko": "“오늘 밤엔 생각이 많아 보이는군!” Darnay가 그녀를 팔로 감싸 안으며 말했다.", "en": "“We are thoughtful tonight!” said Darnay, drawing his arm about her."},
    "P030_1": {"ko": "“네, 사랑하는 Charles,” 그녀는 그의 가슴에 손을 얹고 묻는 듯하면서도 주의 깊은 표정으로 그를 빤히 바라보며 말했다;", "en": "“Yes, dearest Charles,” with her hands on his breast, and the inquiring and attentive expression fixed upon him;"},
    "P030_2": {"ko": "“우리가 오늘 밤 생각이 좀 많은 편이죠, 오늘 밤 마음에 걸리는 일이 하나 있어서요.”", "en": "“we are rather thoughtful tonight, for we have something on our mind tonight.”"},
    "P031_1": {"ko": "“무슨 일인데, 나의 Lucie?”", "en": "“What is it, my Lucie?”"},
    "P032_1": {"ko": "“제가 묻지 말아 달라고 부탁드리면, 더는 캐묻지 않겠다고 약속해 주시겠어요?”", "en": "“Will you promise not to press me with a question if I beg you not to ask it?”"},
    "P033_1": {"ko": "“약속하냐고?", "en": "“Will I promise?"},
    "P033_2": {"ko": "내 사랑에게 내가 약속하지 못할 일이 뭐가 있겠어?”", "en": "What will I not promise to my Love?”"},
    "P034_1": {"ko": "정말이지, 한 손으로는 뺨에서 금발 머리를 넘겨주고, 다른 한 손으로는 자신을 위해 뛰는 그녀의 가슴에 얹은 그가 약속하지 못할 것이 무엇이겠는가!", "en": "What, indeed, with his hand putting aside the golden hair from the cheek, and his other hand against the heart that beat for him!"},
    "P035_1": {"ko": "“제 생각엔, Charles, 불쌍한 Mr.", "en": "“I think, Charles, poor Mr."},
    "P035_2": {"ko": "Carton은 오늘 밤 당신이 그에 대해 표현한 것보다 더 많은 배려와 존중을 받을 자격이 있는 것 같아요.”", "en": "Carton deserves more consideration and respect than you expressed for him tonight.”"}
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
    if batch['batch_id'] == 'book2_ch_20.json__batch0007':
        batch['status'] = 'done'
with open(queue_path, 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)
print("Done batch 7")

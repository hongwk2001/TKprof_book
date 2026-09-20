import json
chapter_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_20.json'
queue_path = 'c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json'

updates = {
    "P018_1": {"ko": "“정말 진심입니다, Mr.", "en": "“Genuine truth, Mr."},
    "P018_2": {"ko": "Darnay, 저를 믿어주십시오!", "en": "Darnay, trust me!"},
    "P018_3": {"ko": "제가 본론에서 벗어났군요;", "en": "I have gone aside from my purpose;"},
    "P018_4": {"ko": "우리가 친구가 되는 것에 대해 이야기하고 있었죠.", "en": "I was speaking about our being friends."},
    "P018_5": {"ko": "이제, 당신도 저를 아실 겁니다;", "en": "Now, you know me;"},
    "P018_6": {"ko": "제가 인간의 더 높고 더 나은 이상을 좇을 능력이 없는 사람이라는 걸 아시겠죠.", "en": "you know I am incapable of all the higher and better flights of men."},
    "P018_7": {"ko": "만약 의심스러우시면 Stryver에게 물어보십시오, 그가 그렇게 말해줄 겁니다.”", "en": "If you doubt it, ask Stryver, and he'll tell you so.”"},
    "P019_1": {"ko": "“저는 그의 도움 없이 저만의 의견을 갖는 것을 더 선호합니다.”", "en": "“I prefer to form my own opinion, without his aid.”"},
    "P020_1": {"ko": "“글쎄요!", "en": "“Well!"},
    "P020_2": {"ko": "어쨌든 당신은 저를 지금까지 단 한 번도 좋은 일을 한 적이 없고, 앞으로도 절대 하지 않을 방탕한 개자식으로 알고 계시지 않습니까.”", "en": "At any rate, you know me as a dissolute dog who has never done any good, and never will.”"}
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
    if batch['batch_id'] == 'book2_ch_20.json__batch0004':
        batch['status'] = 'done'
with open(queue_path, 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)
print("Done batch 4")

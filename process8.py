import json
chapter_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_20.json'
queue_path = 'c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json'

updates = {
    "P036_1": {"ko": "“정말 그래, 내 사랑?", "en": "“Indeed, my own?"},
    "P036_2": {"ko": "왜 그렇게 생각하지?”", "en": "Why so?”"},
    "P037_1": {"ko": "“그게 바로 당신이 저에게 묻지 않기로 한 질문이에요.", "en": "“That is what you are not to ask me."},
    "P037_2": {"ko": "하지만 제 생각엔--아니 전 알아요--그는 그럴 자격이 있어요.”", "en": "But I think—I know—he does.”"},
    "P038_1": {"ko": "“당신이 그렇게 안다면, 그걸로 충분해.", "en": "“If you know it, it is enough."},
    "P038_2": {"ko": "내가 어떻게 해주길 바라지, 나의 전부여?”", "en": "What would you have me do, my Life?”"},
    "P039_1": {"ko": "“당신에게 부탁하고 싶어요, 내 사랑. 항상 그에게 아주 너그럽게 대해 주시고, 그가 없는 곳에서는 그의 허물을 아주 관대하게 덮어주세요.", "en": "“I would ask you, dearest, to be very generous with him always, and very lenient on his faults when he is not by."},
    "P039_2": {"ko": "그에게는 그가 아주, 아주 드물게만 드러내는 마음이 있고, 그 안에 깊은 상처가 있다는 것을 믿어 달라고 부탁드리고 싶어요.", "en": "I would ask you to believe that he has a heart he very, very seldom reveals, and that there are deep wounds in it."},
    "P039_3": {"ko": "여보, 전 그 마음이 피 흘리는 걸 보았거든요.”", "en": "My dear, I have seen it bleeding.”"},
    "P040_1": {"ko": "“제가 그에게 조금이라도 잘못을 저질렀다는 것은,” Charles Darnay가 꽤 놀란 듯 말했다. “제게 너무나 고통스러운 자책이 되는군요.", "en": "“It is a painful reflection to me,” said Charles Darnay, quite astounded, “that I should have done him any wrong."}
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
    if batch['batch_id'] == 'book2_ch_20.json__batch0008':
        batch['status'] = 'done'
with open(queue_path, 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)
print("Done batch 8")

import json
chapter_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_20.json'
queue_path = 'c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json'

updates = {
    "P006_2": {"ko": "하지만, 저는 의례적인 인사말을 하려는 게 아닙니다.", "en": "but I don't mean any figure of speech."},
    "P006_3": {"ko": "사실 제가 친구가 되고 싶다고 말씀드렸지만, 그 역시 제 본심을 정확히 표현한 것은 아닙니다.”", "en": "Indeed, when I say I wish we could be friends, I hardly mean exactly that, either.”"},
    "P007_1": {"ko": "Charles Darnay는--당연하게도--매우 유쾌하고 친근한 태도로 그게 무슨 뜻인지 물었다.", "en": "Charles Darnay—as was natural—asked him, in all good humor and fellowship, what he did mean."},
    "P008_1": {"ko": "“맹세코,” Carton이 미소를 지으며 말했다. “그건 남에게 설명하는 것보다 제 머릿속으로 이해하는 게 더 쉬운 일입니다.", "en": "“Upon my life,” said Carton, smiling, “I find that easier to comprehend in my own mind than to convey to yours."},
    "P008_2": {"ko": "하지만, 한번 설명해 보겠습니다.", "en": "However, let me try."},
    "P008_3": {"ko": "제가 평소보다--더 심하게 취했던 그 유명한 사건 기억하십니까?”", "en": "Do you remember a certain famous occasion when I was more drunk than—than usual?”"},
    "P009_1": {"ko": "“당신이 술을 마셨다는 사실을 내게 억지로 인정하게 만들었던 그 유명한 사건은 기억합니다.”", "en": "“I remember a certain famous occasion when you forced me to confess that you had been drinking.”"},
    "P010_1": {"ko": "“저도 기억합니다.", "en": "“I remember it too."},
    "P010_2": {"ko": "그런 사건들은 제가 항상 기억하고 있기 때문에, 제게는 무거운 저주와도 같습니다.", "en": "The curse of those occasions is heavy upon me, because I always remember them."},
    "P010_3": {"ko": "언젠가 저의 모든 날들이 끝나는 날, 그것이 정상 참작되기를 바랄 뿐입니다!", "en": "I hope it may be taken into account one day, when all my days are at an end!"}
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
    if batch['batch_id'] == 'book2_ch_20.json__batch0001':
        batch['status'] = 'done'
with open(queue_path, 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)
print("Done batch 1")

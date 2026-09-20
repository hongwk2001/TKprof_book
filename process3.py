import json
chapter_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_20.json'
queue_path = 'c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json'

updates = {
    "P014_4": {"ko": "저는 결코 잊지 않았으며, 그렇게 가볍게 대답하신다고 해서 제가 잊는 데 도움이 되지는 않습니다.”", "en": "I have by no means forgotten it, and a light answer does not help me forget it.”"},
    "P015_1": {"ko": "“가벼운 대답이었다면 용서를 구합니다.” Darnay가 대답했다.", "en": "“If it was a light answer,” returned Darnay, “I beg your forgiveness for it."},
    "P015_2": {"ko": "놀랍게도 당신을 너무 괴롭히는 것 같은 그 사소한 일을 돌려 말하려는 것 외에 다른 뜻은 없었습니다.", "en": "I had no other object than to turn aside a slight thing, which, to my surprise, seems to trouble you too much."},
    "P015_3": {"ko": "신사의 명예를 걸고 말씀드리건대, 저는 진작에 그 일을 마음에서 지워버렸습니다.", "en": "I declare to you, on the honor of a gentleman, that I have long dismissed it from my mind."},
    "P015_4": {"ko": "맙소사, 지워버릴 게 뭐 있었겠습니까!", "en": "Good Heaven, what was there to dismiss!"},
    "P015_5": {"ko": "그날 당신이 제게 베풀어준 큰 은혜 중에 기억해야 할 더 중요한 일이 없었겠습니까?”", "en": "Have I had nothing more important to remember, in the great service you rendered me that day?”"},
    "P016_1": {"ko": "“그 큰 은혜에 대해 말씀하시니,” Carton이 말했다. “그런 식으로 말씀하시면, 그것은 그저 직업상의 허세에 불과했다는 점을 고백해야겠군요. 제가 당신을 도왔을 때 당신이 어찌 되든 신경이나 썼는지 모르겠습니다.--오해 마십시오!", "en": "“As to the great service,” said Carton, “I am bound to confess to you, when you speak of it in that way, that it was mere professional claptrap. I don't know that I cared what became of you when I rendered it.--Mind!"},
    "P016_2": {"ko": "제가 그걸 베풀었을 때 그랬다는 말입니다;", "en": "I say when I rendered it;"},
    "P016_3": {"ko": "과거의 일을 말씀드리는 겁니다.”", "en": "I am speaking of the past.”"},
    "P017_1": {"ko": "“당신은 그 은혜를 가볍게 여기시는군요.” Darnay가 대답했다. “하지만 당신의 그 가벼운 대답에 대해 다투지는 않겠습니다.”", "en": "“You make light of the obligation,” returned Darnay, “but I will not quarrel with your light answer.”"}
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
    if batch['batch_id'] == 'book2_ch_20.json__batch0003':
        batch['status'] = 'done'
with open(queue_path, 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)
print("Done batch 3")

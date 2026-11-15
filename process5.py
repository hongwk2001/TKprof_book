import json
chapter_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_20.json'
queue_path = 'c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json'

updates = {
    "P021_1": {"ko": "“‘앞으로도 절대 하지 않을’ 것인지는 저도 잘 모르겠습니다.”", "en": "“I don't know that you ‘never will.’”"},
    "P022_1": {"ko": "“하지만 저는 압니다, 그러니 제 말을 믿으셔야 합니다.", "en": "“But I do, and you must take my word for it."},
    "P022_2": {"ko": "아무튼!", "en": "Well!"},
    "P022_3": {"ko": "당신이 저 같은 쓸모없는 놈, 평판이 좋지 않은 놈이 때를 가리지 않고 드나드는 것을 견디실 수 있다면, 제가 특권층으로서 이곳을 자유롭게 드나들 수 있도록 허락해 주십사 부탁드리고 싶습니다;", "en": "If you could endure having such a worthless fellow, and one of such indifferent reputation, coming and going at odd times, I should ask that I might be permitted to come and go as a privileged person here;"},
    "P022_4": {"ko": "그저 낡고 쓸모없는 (제가 당신과 저 사이에서 발견한 닮은 점만 아니라면, 장식용조차도 못 되는) 가구 정도로 여겨주시길 바랍니다. 오랫동안 곁에 두었다는 이유로 묵인되고, 아무도 눈여겨보지 않는 그런 가구 말입니다.", "en": "that I might be regarded as a useless (and I would add, if it were not for the resemblance I detected between you and me, an unornamental) piece of furniture, tolerated for its old service, and taken no notice of."},
    "P022_5": {"ko": "그 허락을 남용할 일은 없을 겁니다.", "en": "I doubt if I should abuse the permission."},
    "P022_6": {"ko": "일 년에 네 번이라도 그 권리를 행사할 가능성은 백 분의 일도 안 될 겁니다.", "en": "It is a hundred to one that I would avail myself of it four times in a year."},
    "P022_7": {"ko": "감히 말씀드리지만, 그런 권리가 있다는 사실을 아는 것만으로도 저는 만족할 것입니다.”", "en": "It would satisfy me, I dare say, to know that I had it.”"},
    "P023_1": {"ko": "“한번 해보시겠습니까?”", "en": "“Will you try?”"},
    "P024_1": {"ko": "“그 말씀은 결국 제가 말씀드린 그 조건대로 받아들여 주셨다는 뜻이군요.", "en": "“That is another way of saying that I am placed on the footing I have indicated."}
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
    if batch['batch_id'] == 'book2_ch_20.json__batch0005':
        batch['status'] = 'done'
with open(queue_path, 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)
print("Done batch 5")

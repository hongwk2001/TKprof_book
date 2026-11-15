import json
chapter_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_20.json'
queue_path = 'c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json'

updates = {
    "P045_2": {"ko": "만약 그때 어두운 밤거리를 서성이던 고독한 방랑자가 그녀의 이 순결한 고백을 들을 수 있었다면, 그리고 남편을 이토록 사랑하는 그녀의 부드러운 푸른 눈에서 남편이 동정의 눈물을 입맞춤으로 닦아주는 모습을 볼 수 있었다면, 그는 밤하늘을 향해 이렇게 외쳤을지도 모른다--그의 입술에서 처음 나오는 말도 아니었을 그 말을--", "en": "If one forlorn wanderer then pacing the dark streets could have heard her innocent disclosure, and could have seen the drops of pity kissed away by her husband from the soft blue eyes so loving of that husband, he might have cried to the night—and the words would not have parted from his lips for the first time—"},
    "P046_1": {"ko": "“그녀의 아름다운 연민에 신의 축복이 있기를!”", "en": "“God bless her for her sweet compassion!”"}
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
    if batch['batch_id'] == 'book2_ch_20.json__batch0010':
        batch['status'] = 'done'
with open(queue_path, 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)
print("Done batch 10")

import json
chapter_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_20.json'
queue_path = 'c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json'

updates = {
    "P040_2": {"ko": "제가 그에 대해 이렇게까지 생각하지는 못했소.”", "en": "I never thought this of him.”"},
    "P041_1": {"ko": "“여보, 사실이 그래요.", "en": "“My husband, it is so."},
    "P041_2": {"ko": "그가 갱생하기는 어려울 것 같아요;", "en": "I fear he is not to be reclaimed;"},
    "P041_3": {"ko": "이제 그의 성격이나 운명에서 회복될 희망은 거의 없어요.", "en": "there is scarcely a hope that anything in his character or fortunes is reparable now."},
    "P041_4": {"ko": "하지만 저는 확신해요, 그가 선하고 따뜻하고 심지어 관대한 일까지도 해낼 수 있는 사람이라는 걸요.”", "en": "But I am sure that he is capable of good things, gentle things, even magnanimous things.”"},
    "P042_1": {"ko": "길 잃은 사람을 향한 순수한 믿음을 품고 있는 그녀가 너무 아름다워서, 그녀의 남편은 몇 시간이라도 그대로 그녀를 바라볼 수 있을 것 같았다.", "en": "She looked so beautiful in the purity of her faith in this lost man, that her husband could have looked at her as she was for hours."},
    "P043_1": {"ko": "“그리고, 아 내 사랑!” 그녀가 그에게 더 가까이 매달려, 그의 가슴에 머리를 기대고, 두 눈을 들어 그를 바라보며 간청했다. “우리는 행복 속에서 얼마나 강하며, 그는 불행 속에서 얼마나 나약한지 꼭 기억해 주세요!”", "en": "“And, O my dearest Love!” she urged, clinging nearer to him, laying her head upon his breast, and raising her eyes to his, “remember how strong we are in our happiness, and how weak he is in his misery!”"},
    "P044_1": {"ko": "그 간청은 그의 마음에 깊이 와닿았다. “항상 기억하겠소, 내 사랑!", "en": "The supplication touched him home. “I will always remember it, dear Heart!"},
    "P044_2": {"ko": "내가 살아 있는 한 절대 잊지 않겠소.”", "en": "I will remember it as long as I live.”"},
    "P045_1": {"ko": "그는 그 금발 머리 위로 몸을 굽혀 장밋빛 입술에 입을 맞추고, 그녀를 품에 안았다.", "en": "He bent over the golden head, put the rosy lips to his, and folded her in his arms."}
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
    if batch['batch_id'] == 'book2_ch_20.json__batch0009':
        batch['status'] = 'done'
with open(queue_path, 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)
print("Done batch 9")

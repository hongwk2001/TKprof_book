import json
task = json.load(open('task.json', encoding='utf-8'))[0]
ko = task['korean_original']

print("Finding P017 to P025...")
# P016: 12. "It's all nonsense, from start to finish.
# P017: Why, not satisfied with printing lies on paper
# P018: Good heavens, it will be quite a spectacle
# P019: I could see from the old fellow's self-satisfied air
idx = ko.find("그건 다 쓸데없는 헛소리요")
print("P016:", ko[idx:idx+150])

# I need to print out the surrounding text to find the starts
idx2 = ko.find("왜냐하면")
print("idx2:", idx2)
if idx2 != -1:
    print(ko[idx2:idx2+100])
else:
    print("Maybe:", ko[idx+150:idx+400])

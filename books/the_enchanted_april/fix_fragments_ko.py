import os
import glob

replacements = {
    "결코 그런 뜻이 아니라 그저 비유를 하자면 그렇다는...": 
    "결코 그런 뜻이 아니라 그저 비유를 하자면 그렇다는 뜻이었다.",
    
    "그 시절처럼 이 풍경을 바라볼 수만 있다면...": 
    "그 시절처럼 이 풍경을 바라볼 수만 있다면 얼마나 좋을까 싶었다.",
    
    "늘 끊임없이 다정하게 구는 사람들은 정말 사람을 지치게 만든다...": 
    "늘 끊임없이 다정하게 구는 사람들은 정말 사람을 지치게 만드는 법이었다.",
    
    "세상을 떠난 피셔 씨의 삶에서도 그런 순간들이 있었으니...": 
    "세상을 떠난 피셔 씨의 삶에서도 그런 순간들이 있었던 것이다.",
    
    "만약 프레더릭이 곁에만 있다면...": 
    "만약 프레더릭이 곁에만 있다면 얼마나 좋을까 싶었다.",
    
    "제발 입 좀 다물지...": 
    "제발 입 좀 다물었으면 좋았을 텐데 싶었다.",
    
    "저 눈치 없는 처사라니...": 
    "저 눈치 없는 처사라니 참으로 기가 막힐 노릇이었다.",
    
    "하지만 만약에...": 
    "하지만 만약에 그가 온다면 어떨까.",
    
    "발견하게 된다면 얼마나, 얼마나 멋진 일일까...": 
    "발견하게 된다면 얼마나, 얼마나 멋진 일일까 싶었다.",
    
    "그녀는 즐거움에 숨을 깊이 들이마셨다. 이것이야말로...": 
    "그녀는 즐거움에 숨을 깊이 들이마셨다. 이것이야말로 진정한 자유였다.",
    
    "가까이 다가가 향기를 맡아보고 싶었다...": 
    "가까이 다가가 향기를 맡아보고 싶어졌다.",
    
    "그 또한 그녀를 생각하며 그리워하고 있었던 것이다...": 
    "그 또한 그녀를 생각하며 그리워하고 있었던 것이다.",
    
    "과연 드로이트위치 경의 귀한 영애다운...": 
    "과연 드로이트위치 경의 귀한 영애다운 우아하고 의연한 대처였다.",
    
    "오늘 밤은 차라리...": 
    "오늘 밤은 차라리 침묵을 지키는 편이 나았다.",
    
    "아름다움은 사랑을 낳고, 사랑은 당신을 한층 더 아름답게 만든다...": 
    "아름다움은 사랑을 낳고, 사랑은 당신을 한층 더 아름답게 만드는 법이다.",
    
    "자신이 정말 그런 멋진 존재가 될 수만 있다면...": 
    "자신이 정말 그런 멋진 존재가 될 수만 있다면 얼마나 좋을까 싶었다."
}

base_dir = r"d:\git_repo\TKprof_book\books\the_enchanted_april\chapters"
tagged_dir = os.path.join(base_dir, "tagged")

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")

# Run for both raw and tagged
for filepath in glob.glob(os.path.join(base_dir, "ch_*_ko.txt")):
    fix_file(filepath)
for filepath in glob.glob(os.path.join(tagged_dir, "tagged_ch_*_ko.txt")):
    fix_file(filepath)

print("Korean fragment fixes complete.")

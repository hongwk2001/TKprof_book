import os
import glob

replacements = {
    # ch_03
    "하인들을 제외하고": "상주 직원들을 제외하고",
    "하인들의 급여는": "직원들의 급여는",
    # ch_05
    "하인들이 공손하게": "직원들이 공손하게",
    # ch_07
    "하인들을 만나고": "일하는 사람들을 만나고",
    # ch_13
    "하인들이 보기에": "직원들이 보기에",
    "하녀들은 잔소리": "직원들은 잔소리",
    "하인들은 부인들이": "상주 직원들은 부인들이",
    "하인들은 하품을 했다.": "직원들은 하품을 했다.",
    "하인들은 정원이": "일하는 사람들은 정원이",
    # ch_14
    "온 하인들이 매달려야": "모든 직원이 매달려야",
    "하인들에게는 자랑거리이자": "직원들에게는 자랑거리이자",
    "하인들이 보일러 지킨답시고": "일하는 사람들이 보일러 지킨답시고",
    "나머지 하인들은": "나머지 직원들은",
    "하인들의 다급한 고함으로": "직원들의 다급한 고함으로",
    "하인들이 떼로 몰려와": "직원들이 떼로 몰려와",
    "하인들의 코앞에서": "직원들의 코앞에서",
    "하인들의 경고를": "직원들의 경고를",
    "우르르 하인들이 계단을": "우르르 직원들이 계단을",
    "하인들은 폭발음의 정체를": "상주 직원들은 폭발음의 정체를",
    # ch_15
    "하인들이 보기에 그녀는": "직원들이 보기에 그녀는",
    "하인을 물리고": "직원을 물리고",
    # ch_16
    "늙은 하인들뿐이었다": "나이 든 일하는 사람들뿐이었다",
    "늙은 하인들": "나이 든 일하는 사람들",
    "하인들이나 그 누구에": "상주 직원들이나 그 누구에",
    "하인들은 매주": "직원들은 매주",
    # ch_17
    "하인에게 명함을": "직원에게 명함을",
    "하인이 말했다": "직원이 말했다",
    "하인이 물러가자": "직원이 물러가자",
    # ch_18
    "하인들이 어떤지": "일하는 사람들이 어떤지",
    "하인이 쏜살같이": "직원이 쏜살같이",
    # ch_20
    "하인을 보낼게요": "직원을 보낼게요",
}

base_dir = r"d:\git_repo\TKprof_book\books\the_enchanted_april\chapters"
tagged_dir = os.path.join(base_dir, "tagged")

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            modified = True
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")

# Process raw chapters
for filepath in glob.glob(os.path.join(base_dir, "ch_*_ko.txt")):
    process_file(filepath)

# Process tagged chapters
for filepath in glob.glob(os.path.join(tagged_dir, "tagged_ch_*_ko.txt")):
    process_file(filepath)

print("Replacement complete.")

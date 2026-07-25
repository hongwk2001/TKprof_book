import os
import glob
import re

base_dir = r"d:\git_repo\TKprof_book\books\the_enchanted_april\chapters"
tagged_dir = os.path.join(base_dir, "tagged")

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    # Ch 16
    content = content.replace("한 명이—”", "한 명이...”")
    content = content.replace(
        "로티의 인성은—비록 그녀가 똑똑한 남편과 겉보기에 아주 조화롭게 지내고 있다 할지라도—여전히 피셔 부인에게는 완전히 이질적이었으며",
        "비록 로티가 똑똑한 남편과 겉보기에 아주 조화롭게 지내고 있다 할지라도, 그녀의 인성은 여전히 피셔 부인에게는 완전히 이질적이었으며"
    )
    
    # Ch 17
    content = content.replace("갈망했던가—연단 위나", "갈망했던가, 연단 위나")
    content = content.replace("그 나이에 무슨—”", "그 나이에 무슨...”")
    
    # Ch 18
    # "남겼다는 사실을—특히 자신의 성품이나 선행과는 무관하게 외적인 매력으로 남겼다는 사실을—알게 되는 것은 기분 좋은 일이었기에 로즈는 내심 기뻤다."
    # ->
    # "남겼다는 사실을 알게 되는 것은 기분 좋은 일이었기에 로즈는 내심 기뻤다. 특히 자신의 성품이나 선행과는 무관하게 외적인 매력으로 남겼다는 사실을 말이다."
    content = content.replace(
        "남겼다는 사실을—특히 자신의 성품이나 선행과는 무관하게 외적인 매력으로 남겼다는 사실을—알게 되는 것은 기분 좋은 일이었기에 로즈는 내심 기뻤다.",
        "남겼다는 사실을 알게 되는 것은 기분 좋은 일이었기에 로즈는 내심 기뻤다. 특히 자신의 성품이나 선행과는 무관하게 외적인 매력으로 남겼다는 사실을 말이다."
    )
    content = content.replace("자제라니—”", "자제라니...”")
    
    # Ch 21
    # "찰나의 순간—아무리 사랑에 눈이 먼 연인들일지라도 문득 정신이 드는 순간이 있기 마련이다—그는 품 안에 안긴 여인이 다른 곳에 있는 아무리 아름다운 여인보다도 훨씬 더 강력한 힘을 발휘한다는 사실을 깨달았다."
    # ->
    # "찰나의 순간, 그는 품 안에 안긴 여인이 다른 곳에 있는 아무리 아름다운 여인보다도 훨씬 더 강력한 힘을 발휘한다는 사실을 깨달았다. 아무리 사랑에 눈이 먼 연인들일지라도 문득 정신이 드는 순간이 있기 마련인 법이다."
    content = content.replace(
        "찰나의 순간—아무리 사랑에 눈이 먼 연인들일지라도 문득 정신이 드는 순간이 있기 마련이다—그는 품 안에 안긴 여인이 다른 곳에 있는 아무리 아름다운 여인보다도 훨씬 더 강력한 힘을 발휘한다는 사실을 깨달았다.",
        "찰나의 순간, 그는 품 안에 안긴 여인이 다른 곳에 있는 아무리 아름다운 여인보다도 훨씬 더 강력한 힘을 발휘한다는 사실을 깨달았다. 아무리 사랑에 눈이 먼 연인들일지라도 문득 정신이 드는 순간이 있기 마련인 법이다."
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")

# Run for both raw and tagged
for filepath in glob.glob(os.path.join(base_dir, "ch_*_ko.txt")):
    fix_file(filepath)
for filepath in glob.glob(os.path.join(tagged_dir, "tagged_ch_*_ko.txt")):
    fix_file(filepath)

print("Pass 3 dash adaptation complete.")

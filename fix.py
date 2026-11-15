with open('patch_10_14.py', 'r', encoding='utf-8') as f:
    code = f.read()

prefix = '"book3_ch_14.json__batch0010": ['
new_prefix = prefix + '\n        {"ko": "그녀의 허리춤에 몰래 숨겨져 있는 것은, 날이 선 단검이었다.", "en": "Hidden at her waist was a sharpened dagger."},\n'

code = code.replace(prefix, new_prefix)
with open('patch_10_14_fixed.py', 'w', encoding='utf-8') as f:
    f.write(code)

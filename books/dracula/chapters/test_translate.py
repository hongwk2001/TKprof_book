import urllib.request
import urllib.parse
import json

def translate(text):
    q = urllib.parse.quote(text)
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ko&tl=en&dt=t&q={q}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        return ''.join([sentence[0] for sentence in data[0]])
    except Exception as e:
        return str(e)

print(translate("안녕하세요! 이것은 테스트입니다."))

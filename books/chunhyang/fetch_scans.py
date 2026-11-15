"""Download the 완판 84장본 열녀춘향수절가 scans from the National Museum of Korea.

Source: 국립중앙박물관 신수15187, 공공누리 제1유형 (출처표시).
https://www.museum.go.kr/MUSEUM/contents/M0502000000.do?schM=view&searchId=search&relicId=2412
Images land in scans/ (git-ignored); the URL list is recorded in raw/_source.json.
"""
import json
import pathlib
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).parent
BASE = "https://www.museum.go.kr/relic_image/PS01001001/ssu000/2024/"
# image number -> upload folder, as listed on the museum page (relicId=2412)
FOLDERS = """
90000 1220163752346 90001 1220163756636 90002 1220163801002 90003 1220163805504
90004 1220163809952 90005 1220163814046 90006 1220163818453 90007 1220163822969
90008 1220163827374 90009 1220163832243 90010 1220163836716 90011 1220163840968
90012 1220163845725 90013 1220163850166 90014 1220163854618 90015 1220163858760
90016 1220163903181 90017 1220163907595 90018 1220163912022 90019 1220163916407
90020 1220163920555 90021 1220163924651 90022 1220163929055 90023 1220163933778
90024 1220163938158 90025 1220163942574 90026 1220163946962 90027 1220163951406
90028 1220163955493 90029 1220163959883 90030 1220164003976 90031 1220164008401
90032 1220164012514 90033 1220164016934 90034 1220164021348 90035 1220164025788
90036 1220164030212 90037 1220164034294 90038 1220164038743 90039 1220164042839
90040 1220164047242 90041 1220164052010 90042 1220164056574 90043 1220164101020
90044 1220164105463 90045 1220164109954 90046 1220164115945 90047 1220164121947
90048 1220164127950 90049 1220164133949 90050 1220164139949 90051 1220164145941
90052 1220164151952 90053 1220164157943 90054 1220164203942 90055 1220164209944
90056 1220164215948 90057 1220164221943 90058 1220164227948 90059 1220164233951
90060 1220164239941 90061 1220164245941 90062 1220164250327 90063 1220164254348
90064 1220164258716 90065 1220164303145 90066 1220164307289 90067 1220164311396
90068 1220164315782 90069 1220164320302 90070 1220164324840 90071 1220164329301
90072 1220164333892 90073 1220164338238 90074 1220164342662 90075 1220164346799
90076 1220164351178 90077 1220164355297 90078 1220164400940 90079 1220164406949
90080 1220164412949 90081 1220164418950 90082 1220164423335 90083 1220164427734
90084 1220163057561 90085 1220163102045
""".split()


def main():
    pairs = dict(zip(FOLDERS[0::2], FOLDERS[1::2]))
    urls = {n: f"{BASE}{f}/ssu015187-000-{n}.jpg" for n, f in pairs.items()}
    (HERE / "scans").mkdir(exist_ok=True)
    for n, url in urls.items():
        dest = HERE / "scans" / f"{n}.jpg"
        if dest.exists():
            continue
        part = dest.with_suffix(".part")
        for attempt in range(5):  # the museum server drops long transfers
            try:
                urllib.request.urlretrieve(url, part)
                break
            except (urllib.error.ContentTooShortError, OSError) as e:
                print(n, "retry", attempt + 1, e, flush=True)
        else:
            raise SystemExit(f"{n}: gave up after 5 attempts")
        part.replace(dest)  # rename only when complete
        print(n, dest.stat().st_size, flush=True)
    source = {
        "title": "열녀춘향수절가 (烈女春香守節歌), 완판 84장본",
        "edition": "1911, 전주 서계서포(西溪書鋪) 간행 (museum description)",
        "holder": "국립중앙박물관 (National Museum of Korea), 소장품번호 신수15187",
        "page": "https://www.museum.go.kr/MUSEUM/contents/M0502000000.do?schM=view&searchId=search&relicId=2412",
        "license": "공공누리 제1유형 (출처표시) — commercial use allowed with attribution",
        "credit": "원문 이미지: 국립중앙박물관 소장 「열녀춘향수절가」(신수15187), 공공누리 제1유형",
        "transcription": "in-house from the scans",
        "images": urls,
    }
    (HERE / "raw" / "_source.json").write_text(
        json.dumps(source, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()

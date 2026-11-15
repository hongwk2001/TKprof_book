"""Write review/chunhyang_review.html: the whole book on one page for review.

Chapter nav, each chapter's "please check" notes from review_flags.json, and
every passage as numbered Korean/English rows (ids match apply_*.py), with the
old source text tucked into a details box.

    python make_review_html.py
"""
import glob
import html
import json
import pathlib

HERE = pathlib.Path(__file__).parent
FLAGS = json.loads((HERE / "review_flags.json").read_text(encoding="utf-8"))

CSS = """
:root{--bg:#f4f5f3;--paper:#fbfbfa;--ink:#1d2126;--muted:#646b73;--rule:#dfe2e0;
--indigo:#2c4a78;--indigo-soft:#e6ebf3;--seal:#a8382c;--seal-soft:#f6e7e4;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#14171b;--paper:#1b1f24;
--ink:#e3e6e9;--muted:#9aa2ab;--rule:#2c3238;--indigo:#93acd8;--indigo-soft:#222c3b;
--seal:#e3806f;--seal-soft:#3a2522;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#14171b;--paper:#1b1f24;--ink:#e3e6e9;--muted:#9aa2ab;--rule:#2c3238;
--indigo:#93acd8;--indigo-soft:#222c3b;--seal:#e3806f;--seal-soft:#3a2522;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font:16px/1.6 "Literata",Georgia,serif;padding-inline:16px}
.wrap{max-width:1080px;margin:0 auto;padding-block:28px 64px}
header h1{font:600 clamp(28px,5vw,40px)/1.15 "Noto Serif KR",serif;margin:0;text-wrap:balance}
header .sub{color:var(--muted);margin:.4em 0 0;max-width:65ch}
.stats{display:flex;flex-wrap:wrap;gap:8px 20px;margin:16px 0 0;font:13px/1.4 "IBM Plex Mono",monospace;color:var(--muted)}
.stats b{color:var(--ink);font-weight:600}
nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:2;background:var(--bg);
padding-block:10px;margin-top:20px;border-bottom:1px solid var(--rule);display:flex;flex-wrap:wrap;gap:6px}
nav a{font:13px/1 "IBM Plex Mono",monospace;text-decoration:none;color:var(--indigo);
padding:6px 8px;border:1px solid var(--rule);border-radius:4px;background:var(--paper)}
nav a.flag{border-color:var(--seal);color:var(--seal)}
nav a:focus-visible,summary:focus-visible{outline:2px solid var(--indigo);outline-offset:2px}
.tools{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:12px;font-size:14px;color:var(--muted)}
.tools input[type=search]{font:inherit;padding:6px 10px;border:1px solid var(--rule);border-radius:4px;
background:var(--paper);color:var(--ink);min-width:0;flex:1 1 220px}
section.ch{margin-top:44px;scroll-margin-top:110px}
section.ch h2{font:600 24px/1.3 "Noto Serif KR",serif;margin:0;text-wrap:balance}
section.ch h2 small{display:block;font:400 15px/1.4 "Literata",serif;color:var(--muted);margin-top:2px}
.meta{font:12px/1.4 "IBM Plex Mono",monospace;color:var(--muted);margin-top:6px;letter-spacing:.02em}
.check{margin-top:14px;background:var(--seal-soft);border-left:3px solid var(--seal);padding:10px 14px;border-radius:0 4px 4px 0}
.check h3{margin:0 0 4px;font:600 12px/1.4 "IBM Plex Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--seal)}
.check ul{margin:0;padding-left:18px}.check li{margin:2px 0}
.passage{margin-top:18px;background:var(--paper);border:1px solid var(--rule);border-radius:4px;overflow:hidden}
.passage details{border-bottom:1px solid var(--rule);padding:6px 12px;font-size:13px;color:var(--muted)}
.passage summary{cursor:pointer;font:12px/1.6 "IBM Plex Mono",monospace;color:var(--indigo)}
.passage details p{margin:6px 0 4px;font-family:"Noto Serif KR",serif;word-break:break-all}
.bridge{font:12px "IBM Plex Mono",monospace;color:var(--seal);margin-left:8px}
.row{display:grid;grid-template-columns:76px 1fr 1fr;gap:4px 16px;padding:8px 12px;border-top:1px solid var(--rule)}
.row:first-of-type{border-top:0}
.id{font:12px/1.9 "IBM Plex Mono",monospace;color:var(--muted);font-variant-numeric:tabular-nums}
.ko{font-family:"Noto Serif KR",serif;font-size:15px;line-height:1.75}
.en{font-size:15.5px}
mark{background:var(--indigo-soft);color:inherit;padding:0 1px}
@media (max-width:720px){.row{grid-template-columns:1fr}.id{line-height:1.2}}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
"""

JS = """
const q=document.getElementById('q'),only=document.getElementById('only'),count=document.getElementById('count');
function apply(){const t=q.value.trim().toLowerCase();let n=0;
document.querySelectorAll('section.ch').forEach(s=>{const flagged=s.dataset.flag==='1';
let any=false;s.querySelectorAll('.row').forEach(r=>{const hit=!t||r.dataset.t.includes(t);r.hidden=!hit;if(hit){any=true;n++}});
s.querySelectorAll('.passage').forEach(p=>{p.hidden=![...p.querySelectorAll('.row')].some(r=>!r.hidden)});
s.hidden=(only.checked&&!flagged)||!any});
count.textContent=t?n+' matching lines':'';}
q.addEventListener('input',apply);only.addEventListener('change',apply);
"""


def main():
    chapters, total_pairs, total_words = [], 0, 0
    for path in sorted(glob.glob(str(HERE / "json" / "ch_*.json"))):
        rows = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        chapters.append(rows)
        for r in rows:
            total_pairs += len(r["sentences"])
            total_words += sum(len(s["en"].split()) for s in r["sentences"])
    nav, body = [], []
    for rows in chapters:
        h = rows[0]
        ch = h["chapter_id"]
        flags = FLAGS.get(ch, [])
        words = sum(len(s["en"].split()) for r in rows for s in r["sentences"])
        nav.append(f'<a href="#{ch}" class="{"flag" if flags else ""}">{ch[3:]}</a>')
        out = [f'<section class="ch" id="{ch}" data-flag="{1 if flags else 0}">',
               f'<h2>{ch[3:]}. {html.escape(h["ko_title"])}<small>{html.escape(h["en_title"])}</small></h2>',
               f'<div class="meta">Leaves {h["pages"][0]}–{h["pages"][1]} · {sum(len(r["sentences"]) for r in rows)} lines · '
               f'{words:,} words · ~{words / 150:.0f} min</div>']
        if flags:
            out.append('<div class="check"><h3>Please check</h3><ul>' +
                       "".join(f"<li>{html.escape(f)}</li>" for f in flags) + "</ul></div>")
        for r in rows[1:]:
            src = html.escape(r["src"])
            tag = r["tag"] + ('<span class="bridge">editorial bridge</span>' if r.get("editorial") else "")
            out.append(f'<div class="passage"><details><summary>{tag} · original</summary><p>{src}</p></details>')
            for s in r["sentences"]:
                t = html.escape((s["ko"] + " " + s["en"]).lower(), quote=True)
                out.append(f'<div class="row" data-t="{t}"><div class="id">{r["tag"]}.{s["n"]}</div>'
                           f'<div class="ko" lang="ko">{html.escape(s["ko"])}</div>'
                           f'<div class="en" lang="en">{html.escape(s["en"])}</div></div>')
            out.append("</div>")
        out.append("</section>")
        body.append("\n".join(out))
    page = f"""<title>춘향전 Review</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Literata:opsz,wght@7..72,400;7..72,600&family=Noto+Serif+KR:wght@400;600&display=swap">
<style>{CSS}</style>
<div class="wrap">
<header><h1>열녀춘향수절가 · The Tale of Chunhyang</h1>
<p class="sub">Modern Korean and simplified English, side by side, for review. Line ids (P0003.4) are the ones to quote back when asking for a change. Chapters marked in red have items to decide.</p>
<div class="stats"><span><b>21</b> chapters</span><span><b>{total_pairs:,}</b> lines</span><span><b>{total_words:,}</b> English words</span><span><b>~{total_words / 150 / 60:.1f} h</b> at 150 wpm</span><span>source: 완판 84장본, 국립중앙박물관 신수15187</span></div></header>
<nav aria-label="Chapters">{''.join(nav)}</nav>
<div class="tools"><input type="search" id="q" placeholder="Search Korean or English" aria-label="Search lines">
<label><input type="checkbox" id="only"> Only chapters with items to check</label><span id="count"></span></div>
{''.join(body)}
</div>
<script>{JS}</script>
"""
    out = HERE / "review" / "chunhyang_review.html"
    out.write_text(page, encoding="utf-8")
    print(f"{out} {len(page.encode('utf-8')) // 1024} KB, {total_pairs} lines, {total_words} words")


if __name__ == "__main__":
    main()

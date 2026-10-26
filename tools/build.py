"""Builds index.html from the topic sources in tools/. Run: python3 tools/build.py"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.join(HERE, '..'))
import cost_questions, cvp_questions

def read(p): return open(os.path.join('tools', p), encoding='utf-8').read()

def sales_mix(tid):
    s = read('sales_mix.html').replace('<section class="prob">', '<section class="q">')
    s = re.sub(r'id="b(\d)"', rf'class="rv" data-t="{tid}-m\1"', s)
    return re.sub(r'class="ans" id="a(\d)"', rf'class="ans" id="{tid}-m\1"', s)

# Home page order = list order. Each topic gets its own box and its own tabs.
TOPICS = [
    dict(id="cost", title="Cost Concepts & Cost Behavior",
         blurb="Product vs. period costs, COGM and COGS, cost behavior, high-low method",
         handout=read('cost_handout.html'), qs=cost_questions.Q,
         intro="Questions 1 to 40 are four sets of the same 10 problem types (1–10, 11–20, 21–30, 31–40), each with different givens. Solve first, then tap Reveal answer.",
         extra=[]),
    dict(id="cvp", title="CVP Analysis",
         blurb="Break-even, target profit, margin of safety, sales mix, operating leverage",
         handout=read('cvp_handout.html'), qs=cvp_questions.Q,
         intro="Questions 1 to 39 are three sets of the same 13 problem types with new givens. Number 40 is a bonus on the indifference point. Solve first, then tap Reveal answer.",
         extra=[("mix", "Sales Mix (5)", "Sales Mix Problems",
                 "Units of each product needed to break even and to hit profit targets.", sales_mix)]),
]

def qhtml(tid, i, q):
    k = f"{tid}-s{i}"
    out = [f'<section class="q"><div class="qh"><span class="qn">{i}.</span><span class="tag">{q["topic"]}</span></div>',
           f'<div class="stem">{q["stem"]}</div>']
    for p in q["parts"]:
        if p["q"]:
            out.append(f'<p class="sub">{p["q"]}</p>')
        out.append('<ol class="opts" type="a">' + "".join(f"<li>{o}</li>" for o in p["opts"]) + '</ol>')
    out.append(f'<button type="button" class="rv" data-t="{k}">Reveal answer</button><div class="ans" id="{k}" hidden>')
    for p in q["parts"]:
        lab = (p["q"].split(":")[0] + " — ") if p["q"] else ""
        out.append(f'<p class="key">{lab}Answer: <b>{"abcd"[p["ans"]]}. {p["correct"]}</b></p><ul class="steps">' +
                   "".join(f"<li>{s}</li>" for s in p["sol"]) + "</ul>")
    out.append('</div></section>')
    return "".join(out)

boxes, views = [], []
for t in TOPICS:
    tid, n = t["id"], len(t["qs"])
    boxes.append(f'<button type="button" class="sec" data-topic="{tid}"><b>{t["title"]}</b>{t["blurb"]}<small>Handout · {n} questions'
                 + "".join(" · " + e[1] for e in t["extra"]) + '</small></button>')
    tabs = [("handout", "Handout"), ("questions", f"Questions ({n})")] + [(e[0], e[1]) for e in t["extra"]]
    panes = [f'<div class="pane" data-v="handout">{t["handout"]}</div>',
             f'<div class="pane" data-v="questions" hidden><h2>{t["title"]}: Practice Questions</h2><p class="intro">{t["intro"]}</p>'
             + "".join(qhtml(tid, i, q) for i, q in enumerate(t["qs"], 1)) + '</div>']
    for vid, _, h, intro, fn in t["extra"]:
        panes.append(f'<div class="pane" data-v="{vid}" hidden><h2>{h}</h2><p class="intro">{intro}</p>{fn(tid)}</div>')
    views.append(f'<div class="topic" id="t-{tid}" hidden><div class="bar"><button type="button" class="back">← Home</button>'
                 + "".join(f'<button type="button" class="tab" data-v="{v}" aria-selected="{"true" if v == "handout" else "false"}">{l}</button>' for v, l in tabs)
                 + f'</div><p class="crumb">{t["title"]}</p>' + "".join(panes) + '</div>')

page = f'''<title>CVP Practice Hub</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
:root{{--bg:#ffffff;--pink:#ffe4ec;--soft:#fff5f8;--rose:#d94f7c;--deep:#a8315a;--ink:#222222;--muted:#6b5961;--line:#f3c6d5;color-scheme:light}}
*{{box-sizing:border-box}}
[hidden]{{display:none!important}}
body{{background:var(--bg);color:var(--ink);font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:1.6}}
.wrap{{max-width:780px;margin:0 auto;padding-block:20px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
h1{{font-size:26px;color:var(--rose);margin:0 0 4px}}
.sub-h{{color:var(--muted);margin:0 0 22px}}
button{{font-family:Arial,Helvetica,sans-serif;cursor:pointer}}
button:focus-visible{{outline:3px solid var(--ink);outline-offset:2px}}
.sections{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}}
.sec{{text-align:left;background:var(--pink);border:1.5px solid var(--line);border-radius:14px;padding:18px;color:var(--ink);font-size:15px;display:flex;flex-direction:column;gap:4px}}
.sec:hover{{border-color:var(--rose)}}
.sec b{{font-size:19px;color:var(--deep)}}
.sec small{{color:var(--muted);font-size:13px;margin-top:6px}}
.bar{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:6px}}
.back{{background:none;border:0;color:var(--rose);font-size:15px;font-weight:bold;padding:4px 0;margin-right:auto}}
.tab{{background:var(--bg);border:1.5px solid var(--rose);color:var(--deep);border-radius:999px;padding:7px 14px;font-size:14px;font-weight:bold}}
.tab[aria-selected="true"]{{background:var(--rose);color:#ffffff}}
.crumb{{font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin:0 0 14px}}
h2{{font-size:22px;color:var(--rose);margin:0 0 10px}}
.q{{background:var(--soft);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-bottom:16px}}
.q h2{{font-size:18px;margin:0 0 8px}}
.qh{{display:flex;gap:10px;align-items:baseline;margin-bottom:6px}}
.qn{{font-weight:bold;font-size:18px;color:var(--rose)}}
.tag{{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}}
.stem{{min-width:0}}
.sub{{margin:12px 0 4px}}
.opts{{display:grid;grid-template-columns:1fr 1fr;gap:2px 24px;margin:6px 0 12px;padding-left:24px}}
@media (max-width:520px){{.opts{{grid-template-columns:1fr}}}}
.q p{{margin:0 0 8px}}
.q ol[type="a"]:not(.opts){{margin:0 0 12px;padding-left:22px}}
.rv{{font-size:15px;font-weight:bold;background:var(--rose);color:#ffffff;border:0;border-radius:8px;padding:8px 16px}}
.ans{{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px 14px;margin-top:12px}}
.key{{margin:6px 0 4px!important}}
.steps{{margin:0 0 8px;padding-left:20px;font-size:15px}}
.tw{{overflow-x:auto;margin:8px 0 10px}}
table{{border-collapse:collapse;font-variant-numeric:tabular-nums;background:var(--bg);min-width:280px}}
th,td{{padding:5px 12px;border-bottom:1px solid var(--line);text-align:right}}
th:first-child,td:first-child{{text-align:left}}
th{{background:var(--pink);color:var(--deep);font-size:14px}}
.ho h3{{font-size:19px;color:var(--deep);margin:28px 0 8px;padding-bottom:4px;border-bottom:2px solid var(--pink)}}
.ho h4{{font-size:16px;margin:18px 0 6px}}
.ho p,.ho li{{max-width:68ch}}
.ho ul{{padding-left:22px}}
.lead{{font-size:17px}}
.fx{{background:var(--soft);border-left:4px solid var(--rose);border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;display:flex;flex-direction:column;gap:6px}}
.fx span{{font-weight:bold;color:var(--deep);margin-right:4px}}
.tip{{background:var(--pink);border-radius:10px;padding:12px 14px;margin:12px 0}}
table.sum td{{text-align:left;vertical-align:top}}
.intro{{color:var(--muted);margin:0 0 16px}}
.foot{{margin-top:28px;font-size:13px;color:var(--muted);text-align:center}}
</style>

<main class="wrap">
<div id="home">
  <h1>Practice Hub</h1>
  <p class="sub-h">Management Services</p>
  <div class="sections">{"".join(boxes)}</div>
  <p class="foot">Made by Lax</p>
</div>
{"".join(views)}
</main>

<script>
const $=id=>document.getElementById(id);
let cur=null;
function show(tid,v){{
  const t=$("t-"+tid);
  t.querySelectorAll(".tab").forEach(b=>b.setAttribute("aria-selected",b.dataset.v===v?"true":"false"));
  t.querySelectorAll(".pane").forEach(p=>p.hidden=p.dataset.v!==v);
  try{{localStorage.setItem("tab-"+tid,v)}}catch(e){{}}
}}
function openTopic(tid){{
  $("home").hidden=true;document.querySelectorAll(".topic").forEach(t=>t.hidden=t.id!=="t-"+tid);
  let v="handout";try{{v=localStorage.getItem("tab-"+tid)||v}}catch(e){{}}
  if(!$("t-"+tid).querySelector('.pane[data-v="'+v+'"]'))v="handout";
  cur=tid;show(tid,v);window.scrollTo(0,0);
}}
document.querySelectorAll(".sec").forEach(b=>b.onclick=()=>openTopic(b.dataset.topic));
document.querySelectorAll(".back").forEach(b=>b.onclick=()=>{{document.querySelectorAll(".topic").forEach(t=>t.hidden=true);$("home").hidden=false;window.scrollTo(0,0)}});
document.querySelectorAll(".tab").forEach(b=>b.onclick=()=>{{show(cur,b.dataset.v);window.scrollTo(0,0)}});
document.querySelectorAll(".rv").forEach(b=>{{const a=$(b.dataset.t),lab=b.textContent;b.onclick=()=>{{a.hidden=!a.hidden;b.textContent=a.hidden?lab:"Hide answer"+(lab.endsWith("s")?"s":"")}}}});
</script>
'''
open('index.html', 'w', encoding='utf-8').write(page)
print('Built index.html:', ", ".join(f'{t["title"]} {len(t["qs"])} questions' for t in TOPICS))

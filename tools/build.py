import re, sys, html
import os as _o
sys.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from cvp_questions import Q

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
mix = open('tools/sales_mix.html', encoding='utf-8').read()
mix = mix.replace('<section class="prob">', '<section class="q">')
mix = re.sub(r'id="b(\d)"', r'class="rv" data-t="m\1"', mix)
mix = re.sub(r'class="ans" id="a(\d)"', r'class="ans" id="m\1"', mix)
handout = open('tools/cvp_handout.html', encoding='utf-8').read()

def qhtml(i, q):
    out = [f'<section class="q" id="q{i}"><div class="qh"><span class="qn">{i}.</span><span class="tag">{q["topic"]}</span></div>',
           f'<div class="stem">{q["stem"]}</div>']
    for j, p in enumerate(q["parts"]):
        if p["q"]:
            out.append(f'<p class="sub">{p["q"]}</p>')
        out.append('<ol class="opts" type="a">' + "".join(f"<li>{o}</li>" for o in p["opts"]) + '</ol>')
    out.append(f'<button type="button" class="rv" data-t="s{i}">Reveal answer</button><div class="ans" id="s{i}" hidden>')
    for j, p in enumerate(q["parts"]):
        lab = (p["q"].split(":")[0] + " — ") if p["q"] else ""
        out.append(f'<p class="key">{lab}Answer: <b>{"abcd"[p["ans"]]}. {p["correct"]}</b></p><ul class="steps">' +
                   "".join(f"<li>{s}</li>" for s in p["sol"]) + "</ul>")
    out.append('</div></section>')
    return "".join(out)

qs = "".join(qhtml(i, q) for i, q in enumerate(Q, 1))

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
.sections{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}}
.sec{{text-align:left;background:var(--pink);border:1.5px solid var(--line);border-radius:14px;padding:18px;color:var(--ink);font-size:15px}}
.sec:hover{{border-color:var(--rose)}}
.sec b{{display:block;font-size:19px;color:var(--deep);margin-bottom:4px}}
.bar{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:18px}}
.back{{background:none;border:0;color:var(--rose);font-size:15px;font-weight:bold;padding:4px 0;margin-right:auto}}
.tab{{background:var(--bg);border:1.5px solid var(--rose);color:var(--deep);border-radius:999px;padding:7px 14px;font-size:14px;font-weight:bold}}
.tab[aria-selected="true"]{{background:var(--rose);color:#ffffff}}
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
table.sum td:last-child{{text-align:left}}
.intro{{color:var(--muted);margin:0 0 16px}}
.foot{{margin-top:28px;font-size:13px;color:var(--muted);text-align:center}}
</style>

<main class="wrap">
<div id="home">
  <h1>Practice Hub</h1>
  <p class="sub-h">Management Services</p>
  <div class="sections">
    <button type="button" class="sec" id="open-cvp"><b>CVP Analysis</b>Handout, 40 practice questions, and 5 sales mix problems</button>
  </div>
  <p class="foot">Made by Lax</p>
</div>

<div id="cvp" hidden>
  <div class="bar">
    <button type="button" class="back" id="back">← Home</button>
    <button type="button" class="tab" data-v="handout" aria-selected="true">Handout</button>
    <button type="button" class="tab" data-v="questions" aria-selected="false">Questions (40)</button>
    <button type="button" class="tab" data-v="mix" aria-selected="false">Sales Mix (5)</button>
  </div>
  <div id="v-handout">{handout}</div>
  <div id="v-questions" hidden><h2>CVP Practice Questions</h2><p class="intro">Questions 1 to 39 are three sets of the same 13 problem types with new givens. Number 40 is a bonus on the indifference point. Solve first, then tap Reveal answer.</p>{qs}</div>
  <div id="v-mix" hidden><h2>Sales Mix Problems</h2><p class="intro">Units of each product needed to break even and to hit profit targets.</p>{mix}</div>
</div>
</main>

<script>
const $=id=>document.getElementById(id);
function show(v){{
  document.querySelectorAll(".tab").forEach(t=>t.setAttribute("aria-selected",t.dataset.v===v?"true":"false"));
  ["handout","questions","mix"].forEach(x=>$("v-"+x).hidden=x!==v);
  try{{localStorage.setItem("cvp-tab",v)}}catch(e){{}}
}}
$("open-cvp").onclick=()=>{{$("home").hidden=true;$("cvp").hidden=false;let v="handout";try{{v=localStorage.getItem("cvp-tab")||v}}catch(e){{}}show(v);window.scrollTo(0,0)}};
$("back").onclick=()=>{{$("cvp").hidden=true;$("home").hidden=false;window.scrollTo(0,0)}};
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{{show(t.dataset.v);window.scrollTo(0,0)}});
document.querySelectorAll(".rv").forEach(b=>{{const a=$(b.dataset.t),lab=b.textContent;b.onclick=()=>{{a.hidden=!a.hidden;b.textContent=a.hidden?lab:"Hide answer"+(lab.endsWith("s")?"s":"")}}}});
</script>
'''
open('index.html', 'w', encoding='utf-8').write(page)
print('Built index.html:', qs.count('class="q"'), 'questions')

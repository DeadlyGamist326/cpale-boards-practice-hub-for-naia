"""Taxation section: turns the study workbook (tools/tax_source.xlsx) into a contents page plus one page per sheet.
Cross-references like "see the Dividends tab" become links; a return button brings the reader back to the exact spot."""
import html, re
import tax_parse

# Reading order (= contents order and Prev/Next order). (sheet name, slug, display name, one-line description)
GROUPS = [
    ("Start here", [
        ("START HERE", "start", "Start Here", "How to use these notes, the 3-question solver, exam-day rules"),
        ("CHECK THESE", "check", "Check These", "Doubtful or outdated items to confirm with your reviewer"),
    ]),
    ("Quick review", [
        ("RATES", "rates", "Rates Cheat Sheet", "Every rate and number on one page"),
        ("HOOKS", "hooks", "Memory Hooks", "Tricks for the hardest numbers"),
        ("QUIZ", "quiz", "Quiz", "119 questions with reveal answers"),
        ("CALCULATORS", "calc", "Calculators", "Type a number, see the tax"),
    ]),
    ("Income taxation", [
        ("General Principles", "principles", "General Principles", "Powers, limitations, escape from taxation"),
        ("Individuals", "individuals", "Individuals", "Taxpayer types, graduated table, final tax, CGT"),
        ("Corporations", "corporations", "Corporations", "RCIT, MCIT, special corporate rates"),
        ("Dividends", "dividends", "Dividends", "Who pays what on dividends"),
        ("Partnerships", "partnerships", "Partnerships", "Partnerships, co-ownership, joint ventures"),
        ("Gross Income", "gross-income", "Gross Income", "Inclusions and exclusions"),
        ("Deductions", "deductions", "Deductions", "Itemized deductions, OSD, limits"),
        ("Capital Assets", "capital-assets", "Capital Assets", "Capital vs ordinary assets, holding period"),
        ("Installment Reporting", "installment", "Installment Reporting", "Initial payments, contract price, 25% test"),
        ("Fringe Benefits", "fringe", "Fringe Benefits", "FBT, monetary value, de minimis"),
    ]),
    ("Transfer taxes", [
        ("Donors Tax", "donors", "Donor's Tax", "6% over ₱250,000, exempt gifts"),
        ("Estate Tax", "estate", "Estate Tax", "Gross estate, deductions, 6%"),
    ]),
    ("Business taxes", [
        ("VAT", "vat", "Value-Added Tax (VAT)", "12%, zero-rated vs exempt, input VAT"),
        ("OPT", "opt", "Other Percentage Tax (OPT)", "3% and special percentage taxes"),
        ("Excise Tax", "excise", "Excise Tax", "Categories of excise taxes"),
        ("DST", "dst", "Documentary Stamp Tax (DST)", "Documents and rates"),
    ]),
    ("Local taxes and incentives", [
        ("Local Taxes", "local", "Local Taxes", "LGC principles, RPT, assessment levels"),
        ("Preferential Taxes", "preferential", "Preferential Taxes", "Incentives and special regimes"),
        ("CREATE MORE", "create-more", "CREATE MORE", "Incentives for registered business enterprises"),
    ]),
    ("Remedies and compliance", [
        ("Remedies", "remedies", "Remedies", "BIR powers, penalties, protest timelines"),
        ("Filing", "filing", "Filing", "Who files, where and when"),
    ]),
    ("Law updates", [
        ("Updates (EOPTA CMEPA)", "updates", "Updates: EOPTA & CMEPA", "What changed in the law"),
        ("CREATE vs TRAIN", "create-train", "CREATE vs TRAIN", "Old vs current rates"),
    ]),
]
PRIORITY = {"rates": 3, "hooks": 3, "quiz": 3, "calc": 3, "check": 3, "updates": 3, "create-more": 3, "create-train": 3,
            "individuals": 3, "corporations": 3, "gross-income": 3, "deductions": 3, "vat": 3, "opt": 3, "estate": 3, "donors": 3, "remedies": 3,
            "dividends": 2, "fringe": 2, "capital-assets": 2, "installment": 2, "partnerships": 2,
            "local": 2, "preferential": 2, "filing": 2, "excise": 2, "dst": 2, "principles": 1}
PRIO_LABEL = {3: "High", 2: "Medium", 1: "Lighter"}

ORDER = [p for _, items in GROUPS for p in items]
SLUG = {sheet: slug for sheet, slug, _, _ in ORDER}
NAME = {slug: name for _, slug, name, _ in ORDER}

# Words used in the notes to point at another tab -> page slug
ALIASES = {
    "START HERE": "start", "CHECK THESE": "check", "RATES": "rates", "HOOKS": "hooks", "QUIZ": "quiz", "CALCULATORS": "calc",
    "General Principles": "principles", "Individuals": "individuals", "Corporations": "corporations", "Dividends": "dividends",
    "Partnerships": "partnerships", "Gross Income": "gross-income", "Deductions": "deductions", "Capital Assets": "capital-assets",
    "Capital": "capital-assets", "Installment Reporting": "installment", "Installment": "installment", "Fringe Benefits": "fringe",
    "Fringe": "fringe", "Donors Tax": "donors", "Donor's Tax": "donors", "Donors": "donors", "Estate Tax": "estate", "Estate": "estate",
    "VAT": "vat", "OPT": "opt", "Excise Tax": "excise", "Excise": "excise", "DST": "dst", "Local Taxes": "local", "Local": "local",
    "Preferential Taxes": "preferential", "Preferential": "preferential", "CREATE MORE": "create-more", "Remedies": "remedies",
    "Filing": "filing", "EOPTA": "updates", "CMEPA": "updates", "Updates": "updates", "CREATE vs TRAIN": "create-train",
    "General": "principles",
}
_alias_re = "|".join(re.escape(a) for a in sorted(ALIASES, key=len, reverse=True))
TAB_REF = re.compile(rf"\b({_alias_re})(?=(?:'|&#x27;)?\s+(?:tabs?\b|and\s+(?:{_alias_re})\s+tabs\b))(?:(?:'|&#x27;)?(\s+tab),\s*Section\s+([A-Z]))?")
CHECK_REF = re.compile(r"CHECK THESE\s*#(\d+)")

def link(slug, label, sec=None):
    h = f"tax-{slug}" + (f"--{sec}" if sec else "")
    return f'<a class="xl" href="#{h}">{label}</a>'

def fmt(text, links=True, all_aliases=False):
    s = html.escape(text)
    s = re.sub(r"\bP(?=\d)", "₱", s)
    if links:
        s = CHECK_REF.sub(lambda m: link("check", m.group(0), "i" + m.group(1)), s)
        if all_aliases:
            s = re.sub(rf"\b({_alias_re})\b", lambda m: link(ALIASES[m.group(1)], m.group(1)), s)
        else:
            def tabref(m):
                if m.group(3):
                    return link(ALIASES[m.group(1)], f"{m.group(1)}{m.group(2)}, Section {m.group(3)}", m.group(3).lower())
                return link(ALIASES[m.group(1)], m.group(1))
            s = TAB_REF.sub(tabref, s)
    return s.replace("\n", "<br>")

def cell_html(c, **kw):
    if not c: return ""
    t = fmt(c["text"], **kw)
    if c.get("red"): return f'<strong class="mem">{t}</strong>'
    if c.get("blue"): return f'<span class="added-t">{t}</span>'
    if c.get("bold"): return f"<b>{t}</b>"
    return t

def sec_key(text, n):
    m = re.match(r"^([A-Z]\d?|\d+)\.\s", text)
    return m.group(1).lower() if m else f"s{n}"

def render_table(b, slug):
    head, rows = b["head"], b["rows"]
    ncol = len(head)
    longest = max((len(c["text"]) for r in rows for c in r if c), default=0)
    stack = ncol >= 3 and longest > 40
    is_tabmap = slug == "start" and head and head[0] == "Tab"
    is_check = slug == "check" and head and head[0] == "#"
    out = [f'<div class="tw"><table class="tx{" st" if stack else ""}">']
    if any(head):
        out.append("<thead><tr>" + "".join(f"<th>{fmt(h, links=False)}</th>" for h in head) + "</tr></thead>")
    out.append("<tbody>")
    for r in rows:
        rid = f' id="tax-check--i{r[0]["text"]}"' if is_check and r[0] else ""
        tds = []
        for i, c in enumerate(r):
            lab = f' data-label="{html.escape(head[i])}"' if stack and head[i] else ""
            tds.append(f"<td{lab}>{cell_html(c, all_aliases=(is_tabmap and i == 0))}</td>")
        out.append(f"<tr{rid}>" + "".join(tds) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)

BAND = {"hook": "Hook", "trap": "Trap", "added": "Added note · verify"}

def render_blocks(blocks, slug):
    out, toc, n, i = [], [], 0, 0
    while i < len(blocks):
        b = blocks[i]; k = b["kind"]
        if k == "title":
            pass
        elif k == "bigidea":
            out.append(f'<div class="big"><span class="lbl">The big idea</span>{fmt(b["text"])}</div>')
        elif k == "note":
            out.append(f'<p class="note">{fmt(b["text"])}</p>')
        elif k == "heading":
            n += 1; key = sec_key(b["text"], n)
            out.append(f'<h3 id="tax-{slug}--{key}">{fmt(b["text"], links=False)}</h3>')
            toc.append((key, re.sub(r"^([A-Z]\d?|\d+)\.\s*", "", b["text"]).split(" - ")[0].split(" (")[0]))
        elif k == "table":
            out.append(render_table(b, slug))
        elif k in BAND:
            out.append(f'<div class="band {k}"><span class="lbl">{BAND[k]}</span>{fmt(b["text"])}</div>')
        elif k == "fivehead":
            items = []
            while i + 1 < len(blocks) and blocks[i + 1]["kind"] == "five":
                i += 1; items.append(re.sub(r"^\d+\.\s*", "", blocks[i]["text"]))
            out.append('<div class="five"><span class="lbl">If you only remember 5 things</span><ol>'
                       + "".join(f"<li>{fmt(t)}</li>" for t in items) + "</ol></div>")
        elif k == "bullet":
            items = []
            while i < len(blocks) and blocks[i]["kind"] == "bullet":
                items.append(cell_html(blocks[i]["cell"] | {"text": blocks[i]["text"]})); i += 1
            i -= 1
            out.append("<ul class=\"bl\">" + "".join(f"<li>{t}</li>" for t in items) + "</ul>")
        elif k == "para":
            out.append(f"<p>{cell_html(b['cell'])}</p>")
        i += 1
    return "".join(out), toc

def render_quiz(blocks):
    t = [b for b in blocks if b["kind"] == "table"][0]
    topics = []
    cards = []
    for n, (tp, q, a) in enumerate(t["rows"], 1):
        topic = tp["text"]
        if topic not in topics: topics.append(topic)
        tslug = ALIASES.get(topic, ALIASES.get(topic.replace("'", "")))
        chip = link(tslug, html.escape(topic)) if tslug else html.escape(topic)
        cards.append(f'<section class="q tq" data-topic="{html.escape(topic)}"><div class="qh"><span class="qn">{n}.</span><span class="tag">{chip}</span></div>'
                     f'<p>{fmt(q["text"])}</p><button type="button" class="rv" data-t="tax-q{n}">Show answer</button>'
                     f'<div class="ans" id="tax-q{n}" hidden>{fmt(a["text"])}</div></section>')
    opts = '<option value="">All topics (119)</option>' + "".join(
        f'<option value="{html.escape(tp)}">{html.escape(tp)} ({sum(1 for r in t["rows"] if r[0]["text"] == tp)})</option>' for tp in topics)
    return ('<div class="big"><span class="lbl">How to use</span>Read the question and say the answer out loud before you tap Show answer. '
            'Put every miss on your redo list and retest only those. Tap a topic label to open its notes.</div>'
            f'<label class="filter" for="tax-qf">Topic <select id="tax-qf">{opts}</select></label>' + "".join(cards))

def render_calc(blocks):
    notes = [b["text"] for b in blocks if b["kind"] == "note"]
    return ('<div class="big"><span class="lbl">How to use</span>Change any number in the boxes and the answers update right away. '
            'Every calculator starts with a worked example. Rates follow the ' + link("rates", "Rates Cheat Sheet") + '.</div>'
            '<div id="tax-calcs"></div>' + (f'<p class="note">{fmt(notes[-1])}</p>' if len(notes) > 1 else ""))

CALC_JS = r"""
const peso=v=>typeof v==="string"?v:"₱"+(Math.round(v*100)/100).toLocaleString("en-US",{maximumFractionDigits:2});
const pct=v=>(Math.round(v*10000)/100)+"%";
const BR=[[0,0,0],[250000,.15,0],[400000,.2,22500],[800000,.25,102500],[2000000,.3,402500],[8000000,.35,2202500]];
function grad(x){let i=0;BR.forEach((r,k)=>{if(x>=r[0])i=k});const r=BR[i],up=BR[i+1],tax=r[2]+r[1]*(x-r[0]);
 return {r,tax,where:peso(x)+" falls in the bracket "+(i===0?"up to ₱250,000":"over "+peso(r[0])+(up?" to "+peso(up[0]):"")),
  steps:i===0?[peso(x)+" is ₱250,000 or less, so the tax is ₱0"]:[peso(r[2])+" + "+pct(r[1])+" × ("+peso(x)+" − "+peso(r[0])+")","= "+peso(r[2])+" + "+pct(r[1])+" × "+peso(x-r[0]),"= "+peso(r[2])+" + "+peso(r[1]*(x-r[0])),"= "+peso(tax)]}}
const CALCS=[
 {t:"A. Individual graduated income tax (2023 onward)",link:["individuals","Individuals"],f:[["nti","Net taxable income",1240000]],
  run:v=>{const g=grad(v.nti);return [
   ["Bracket floor",peso(g.r[0]),0,[g.where]],
   ["Fixed amount + rate × excess",peso(g.r[2])+" + "+pct(g.r[1])+" × "+peso(v.nti-g.r[0]),0,["Fixed amount at the floor: "+peso(g.r[2]),"Rate on the excess: "+pct(g.r[1]),"Excess = "+peso(v.nti)+" − "+peso(g.r[0])+" = "+peso(v.nti-g.r[0])]],
   ["Income tax due",peso(g.tax),1,g.steps]]}},
 {t:"A2. 8% option (self-employed or mixed income)",link:["individuals","Individuals"],f:[["gs","Gross sales/receipts",2500000],["oth","Other non-operating income",0],["mix","Mixed income earner? (1 = yes, 0 = no)",1],["comp","Taxable compensation income (for the mixed earner)",1240000],["wh","Tax withheld on compensation",262000]],
  run:v=>{if(v.gs>3000000)return [["8% income tax","Not eligible: gross sales over ₱3M",1,[peso(v.gs)+" is more than ₱3,000,000, so the 8% option cannot be used; use the graduated table"]]];
   const ded=v.mix==1?0:250000,base=Math.max(0,v.gs+v.oth-ded),t8=.08*base;
   const r=[["8% base",peso(base),0,[peso(v.gs)+" + "+peso(v.oth)+" − "+peso(ded)+(v.mix==1?" (a mixed earner does not deduct ₱250,000)":""),"= "+peso(base)]],
    ["8% income tax",peso(t8),1,["8% × "+peso(base),"= "+peso(t8)]]];
   if(v.mix==1){const g=grad(v.comp);r.push(["Tax on compensation (graduated)",peso(g.tax),0,[g.where].concat(g.steps)],
    ["Total income tax",peso(g.tax+t8),0,[peso(g.tax)+" + "+peso(t8),"= "+peso(g.tax+t8)]],
    ["Tax still payable after withholding",peso(g.tax+t8-v.wh),1,[peso(g.tax+t8)+" − "+peso(v.wh),"= "+peso(g.tax+t8-v.wh)]])}return r}},
 {t:"B. Regular corporate income tax vs MCIT",link:["corporations","Corporations"],f:[["gi","Gross income (sales − cost of sales)",4000000],["ded","Allowable deductions",2000000],["small","Small corporation? (1 = NTI ₱5M or below and assets ₱100M or below)",0]],
  run:v=>{const ti=v.gi-v.ded,r=v.small==1?.2:.25,rcit=Math.max(0,ti)*r,mcit=.02*v.gi,hi=Math.max(rcit,mcit);return [
   ["Taxable income",peso(ti),0,[peso(v.gi)+" − "+peso(v.ded),"= "+peso(ti)]],
   ["RCIT ("+pct(r)+")",peso(rcit),0,[pct(r)+" × "+peso(Math.max(0,ti))+(v.small==1?" (small corporation)":""),"= "+peso(rcit)]],
   ["MCIT (2% of gross income)",peso(mcit),0,["2% × "+peso(v.gi),"= "+peso(mcit)]],
   ["Tax due = higher of the two",peso(hi)+(mcit>rcit?" (MCIT)":" (RCIT)"),1,["Higher of RCIT "+peso(rcit)+" and MCIT "+peso(mcit),"= "+peso(hi)]]]}},
 {t:"C. Fringe benefits tax",link:["fringe","Fringe Benefits"],f:[["mv","Monetary value of the benefit",100000],["rate","FBT rate (0.35 for most; 0.25 for NRA-NETB)",.35]],
  run:v=>{const g=v.mv/(1-v.rate);return [
   ["Grossed-up monetary value = MV ÷ (1 − rate)",peso(g),0,[peso(v.mv)+" ÷ (100% − "+pct(v.rate)+")","= "+peso(v.mv)+" ÷ "+pct(1-v.rate),"= "+peso(g)]],
   ["Fringe benefits tax",peso(g*v.rate),1,[peso(g)+" × "+pct(v.rate),"= "+peso(g*v.rate)]]]}},
 {t:"D. Donor's tax",link:["donors","Donor's Tax"],f:[["g","Total net gifts in the calendar year",750000]],
  run:v=>{const tx=Math.max(0,v.g-250000);return [
   ["Taxable gifts (over ₱250,000)",peso(tx),0,[peso(v.g)+" − ₱250,000","= "+peso(tx)]],
   ["Donor's tax (6%)",peso(.06*tx),1,["6% × "+peso(tx),"= "+peso(.06*tx)]]]}},
 {t:"E. Estate tax (married decedent)",link:["estate","Estate Tax"],f:[["ex","Gross estate: exclusive property",19000000],["cp","Gross estate: conjugal/community property",26000000],["dex","Ordinary deductions: exclusive",1000000],["dcp","Ordinary deductions: conjugal/community",3000000],["fh","Family home included in gross estate",10000000],["ra","Amount received by heirs under RA 4917",0]],
  run:v=>{const ge=v.ex+v.cp,after=ge-v.dex-v.dcp,sp=(v.cp-v.dcp)/2,fh=Math.min(v.fh,10000000),spec=5000000+fh+v.ra+sp,te=Math.max(0,after-spec);return [
   ["Gross estate",peso(ge),0,[peso(v.ex)+" + "+peso(v.cp),"= "+peso(ge)]],
   ["After ordinary deductions",peso(after),0,[peso(ge)+" − "+peso(v.dex)+" − "+peso(v.dcp),"= "+peso(after)]],
   ["Surviving spouse's share (half of net conjugal)",peso(sp),0,["("+peso(v.cp)+" − "+peso(v.dcp)+") ÷ 2","= "+peso(v.cp-v.dcp)+" ÷ 2","= "+peso(sp)]],
   ["Special deductions",peso(spec),0,["Standard ₱5,000,000 + family home "+peso(fh)+(v.fh>10000000?" (capped)":"")+" + RA 4917 "+peso(v.ra)+" + spouse's share "+peso(sp),"= "+peso(spec)]],
   ["Taxable estate",peso(te),0,[peso(after)+" − "+peso(spec),"= "+peso(te)]],
   ["Estate tax (6%)",peso(.06*te),1,["6% × "+peso(te),"= "+peso(.06*te)]]]}},
 {t:"F. VAT payable",link:["vat","VAT"],f:[["vs","Vatable sales (exclusive of VAT)",1000000],["zr","Zero-rated sales",200000],["iv","Total creditable input VAT",0]],
  run:v=>{const o=.12*v.vs,p=o-v.iv;return [
   ["Output VAT (12% of vatable sales)",peso(o),0,["12% × "+peso(v.vs),"= "+peso(o)]],
   ["Zero-rated sales (0% VAT)",peso(0),0,["0% × "+peso(v.zr)+" = ₱0","Input VAT on zero-rated sales can still be claimed"]],
   ["VAT payable",p<0?peso(-p)+" excess input VAT (carry over or refund)":peso(p),1,[peso(o)+" − "+peso(v.iv),"= "+peso(p)+(p<0?" (negative: excess input VAT)":"")]]]}},
 {t:"G. Installment sale",link:["installment","Installment Reporting"],f:[["sp","Selling price",1000000],["cost","Cost of property",600000],["mort","Mortgage assumed by buyer (0 if none)",700000],["dp","Downpayment + other payments in the year of sale",100000]],
  run:v=>{const ex=Math.max(0,v.mort-v.cost),ip=v.dp+ex,cp=v.sp-v.mort+ex,gp=v.sp-v.cost,ratio=ip/v.sp;return [
   ["Excess of mortgage over cost",peso(ex),0,[v.mort>v.cost?peso(v.mort)+" − "+peso(v.cost)+" = "+peso(ex):"Mortgage "+peso(v.mort)+" is not more than cost "+peso(v.cost)+", so ₱0"]],
   ["Initial payments (IP)",peso(ip),0,[peso(v.dp)+" + "+peso(ex),"= "+peso(ip)]],
   ["IP ÷ SP",pct(ratio)+(ratio<=.25?" — 25% test passed":" — over 25%: installment method not allowed"),0,[peso(ip)+" ÷ "+peso(v.sp),"= "+pct(ratio)+(ratio<=.25?" ≤ 25%":" > 25%")]],
   ["Contract price",peso(cp),0,[peso(v.sp)+" − "+peso(v.mort)+" + "+peso(ex),"= "+peso(cp)]],
   ["Gross profit",peso(gp),0,[peso(v.sp)+" − "+peso(v.cost),"= "+peso(gp)]],
   ["Gross profit rate (GP ÷ CP)",pct(gp/cp),0,[peso(gp)+" ÷ "+peso(cp),"= "+pct(gp/cp)]],
   ["Income realized in the year of sale",peso(gp/cp*ip),1,[pct(gp/cp)+" × "+peso(ip),"= "+peso(gp/cp*ip)]]]}},
 {t:"H. Vanishing deduction percentage",link:["estate","Estate Tax"],f:[["y","Years between the two deaths (or gift and death)",2.5]],
  run:v=>{const y=v.y,p=y<=1?1:y<=2?.8:y<=3?.6:y<=4?.4:y<=5?.2:0,band=y<=1?"1 year or less":y<=5?"more than "+(Math.ceil(y)-1)+" but not more than "+Math.ceil(y)+" years":"more than 5 years";return [
   ["Percentage allowed",pct(p),1,[y+" years is "+band,"→ "+pct(p)]],
   ["Scale","100 / 80 / 60 / 40 / 20%, none after 5 years"]]}},
];
const DN=[
 ["<b>Already taken out.</b> Enter the NET taxable income, after deductions.",
  "<b>Self-employed or professional:</b> Gross sales/receipts − Cost of sales = Gross income, then subtract EITHER itemized deductions OR the OSD (40% of gross sales/receipts). Choose only one.",
  "<b>Purely an employee:</b> no business deductions. Only exclusions are removed: 13th month pay and other benefits up to ₱90,000, de minimis benefits, and SSS/PhilHealth/Pag-IBIG contributions."],
 ["<b>None.</b> The 8% is applied to GROSS sales/receipts, so itemized deductions and the OSD are not allowed. That is the trade-off for a simple flat rate.",
  "The only thing subtracted is ₱250,000, and only for a purely self-employed person. A mixed income earner already used it on compensation.",
  "Choose 8% when business expenses are small. When expenses are big, graduated rates + deductions usually give a lower tax."],
 ["<b>RCIT: yes.</b> Allowable deductions (itemized, or OSD at 40% of GROSS INCOME for corporations) are subtracted to get taxable income.",
  "<b>MCIT: none.</b> It is 2% of GROSS income on purpose: a floor so a company with large deductions or a loss still pays some tax."],
 ["<b>None in computing FBT.</b> The tax is on the monetary value of the benefit, grossed up.",
  "For the employer, the benefit and the FBT paid are deductible business expenses in its own income tax."],
 ["<b>Only the ₱250,000 yearly exemption.</b> Donor's tax has no expense-type deductions.",
  "Use NET gifts: the value of the gift less any debt or mortgage the donee assumes. Exempt gifts (for example, to the government or accredited non-profits) are left out of total gifts."],
 ["<b>Yes, two kinds.</b> Ordinary deductions (claims against the estate, losses, unpaid mortgage, transfers for public use), split into exclusive and conjugal.",
  "Special deductions: ₱5,000,000 standard, family home up to ₱10,000,000, RA 4917 benefits. The surviving spouse's share is also removed because it never belonged to the decedent."],
 ["<b>No deductions in VAT.</b> Instead, input VAT paid on purchases is CREDITED against output VAT.",
  "Only a VAT-registered seller with valid VAT invoices or receipts can claim input VAT."],
 ["<b>Not a tax yet, so no deductions here.</b> This only decides how much of the gain is reported this year.",
  "The income realized goes into gross income, where the regular deductions apply."],
 ["<b>This percentage is itself a deduction</b> in estate tax (the vanishing deduction, or property previously taxed).",
  "It reduces the estate for property the decedent received by inheritance or gift within 5 years before death, so the same property is not fully taxed twice."],
];
const FX=[
 ["<b>Income tax</b> = Fixed amount at the bracket floor + Rate × (Net taxable income − Bracket floor)",
  "Brackets: up to ₱250,000 → 0% · over ₱250,000 → 15% · over ₱400,000 → ₱22,500 + 20% · over ₱800,000 → ₱102,500 + 25% · over ₱2M → ₱402,500 + 30% · over ₱8M → ₱2,202,500 + 35%"],
 ["<b>Purely self-employed:</b> 8% × (Gross sales/receipts + Other non-operating income − ₱250,000)",
  "<b>Mixed income earner:</b> Graduated tax on compensation + 8% × (Gross sales/receipts + Other income), with NO ₱250,000 deduction",
  "<b>Tax still payable</b> = Total income tax − Tax withheld",
  "Allowed only if gross sales/receipts do not exceed ₱3,000,000"],
 ["<b>Taxable income</b> = Gross income − Allowable deductions",
  "<b>RCIT</b> = 25% × Taxable income (20% for a small corporation)",
  "<b>MCIT</b> = 2% × Gross income",
  "<b>Tax due</b> = whichever is HIGHER, RCIT or MCIT"],
 ["<b>Grossed-up monetary value</b> = Monetary value ÷ (100% − FBT rate)",
  "<b>FBT</b> = Grossed-up monetary value × FBT rate",
  "At 35%: FBT = Monetary value ÷ 65% × 35%"],
 ["<b>Donor's tax</b> = 6% × (Total net gifts in the calendar year − ₱250,000)"],
 ["<b>Gross estate</b> = Exclusive property + Conjugal/community property",
  "<b>Surviving spouse's share</b> = ½ × (Conjugal property − Conjugal deductions)",
  "<b>Special deductions</b> = ₱5,000,000 standard + Family home (max ₱10,000,000) + RA 4917 benefits + Spouse's share",
  "<b>Taxable estate</b> = Gross estate − Ordinary deductions − Special deductions",
  "<b>Estate tax</b> = 6% × Taxable estate"],
 ["<b>Output VAT</b> = 12% × Vatable sales (zero-rated sales × 0%)",
  "<b>VAT payable</b> = Output VAT − Creditable input VAT",
  "If the result is negative, it is excess input VAT to carry over or refund"],
 ["<b>Initial payments (IP)</b> = Downpayment + Other payments in the year of sale + Excess of mortgage over cost",
  "<b>25% test:</b> IP ÷ Selling price must be 25% or less",
  "<b>Contract price</b> = Selling price − Mortgage assumed + Excess of mortgage over cost",
  "<b>Gross profit rate</b> = Gross profit ÷ Contract price",
  "<b>Income realized</b> = Gross profit rate × Collections in the year (IP in the year of sale)"],
 ["<b>Vanishing deduction %</b> depends on the years between the two transfers:",
  "1 year or less → 100% · up to 2 → 80% · up to 3 → 60% · up to 4 → 40% · up to 5 → 20% · over 5 → none"],
];
function buildCalcs(){const box=$("tax-calcs");if(!box||box.dataset.done)return;box.dataset.done=1;
 CALCS.forEach((c,ci)=>{const s=document.createElement("section");s.className="calc";
  s.innerHTML='<h3>'+c.t+'</h3><div class="fx calcfx"><span class="lbl">Formula</span>'+FX[ci].map(l=>'<div>'+l+'</div>').join("")+'</div><div class="dn"><span class="lbl">Deductions</span>'+DN[ci].map(l=>'<div>'+l+'</div>').join("")+'</div>'+c.f.map(f=>'<label class="cf" for="c'+ci+f[0]+'"><span>'+f[1]+'</span><input id="c'+ci+f[0]+'" type="number" inputmode="decimal" step="any" value="'+f[2]+'"></label>').join("")
   +'<div class="out"></div><p class="calc-l">Notes: <a class="xl" href="#tax-'+c.link[0]+'">'+c.link[1]+'</a></p>';
  box.appendChild(s);const upd=()=>{const v={};c.f.forEach(f=>v[f[0]]=parseFloat($("c"+ci+f[0]).value)||0);
   s.querySelector(".out").innerHTML=c.run(v).map((r,ri)=>'<div class="row'+(r[2]?" res":"")+'"><span>'+r[0]+'</span><b>'+r[1]+'</b>'
     +(r[3]?'<button type="button" class="wk" aria-expanded="false" aria-label="Show the computation for '+r[0].replace(/"/g,"")+'">=</button><div class="work" hidden><span class="lbl">Computation</span>'+r[3].map(x=>'<div>'+x+'</div>').join("")+'</div>':'')+'</div>').join("")};
  const out=s.querySelector(".out"),hov=matchMedia("(hover: hover)").matches;
  const closeAll=()=>{s.querySelectorAll(".work").forEach(x=>{x.hidden=true;delete x.dataset.pin});s.querySelectorAll(".wk").forEach(x=>x.setAttribute("aria-expanded","false"))};
  out.addEventListener("click",e=>{const row=e.target.closest(".row");if(!row||!(e.target.closest(".wk")||e.target.closest(".row > b")))return;
   const w=row.querySelector(".work"),b=row.querySelector(".wk");if(!w)return;const pinned=w.dataset.pin==="1";closeAll();
   if(!pinned){w.hidden=false;w.dataset.pin="1";b.setAttribute("aria-expanded","true")}});
  if(hov){out.addEventListener("mouseover",e=>{const v=e.target.closest(".row > b");if(!v)return;const w=v.parentElement.querySelector(".work");if(w&&w.hidden){w.hidden=false;w.dataset.hov="1"}});
   out.addEventListener("mouseout",e=>{const v=e.target.closest(".row > b");if(!v||v.contains(e.relatedTarget))return;const w=v.parentElement.querySelector(".work");if(w&&w.dataset.hov&&w.dataset.pin!=="1"){w.hidden=true}if(w)delete w.dataset.hov});}
  s.querySelectorAll("input").forEach(i=>i.addEventListener("input",upd));upd()})}
"""

def render():
    pages = dict(tax_parse.load())
    title_fix = lambda t: re.sub(r"\s*\(revised from your [^)]*\)", "", t)
    views = []
    # contents
    groups_html = []
    for g, items in GROUPS:
        lis = "".join(f'<li><a class="xl toc" href="#tax-{slug}"><span class="tn">{name}</span><span class="td">{fmt(desc, links=False)}</span>'
                      + (f'<span class="pr p{PRIORITY[slug]}">{PRIO_LABEL[PRIORITY[slug]]}</span>' if slug in PRIORITY else "") + '</a></li>' for _, slug, name, desc in items)
        groups_html.append(f'<h3>{g}</h3><ul class="toclist">{lis}</ul>')
    legend = ('<div class="legend"><span><strong class="mem">Red bold</strong> memorize</span><span class="lg hook">Hook</span>'
              '<span class="lg trap">Trap</span><span class="lg five">5 things</span><span class="lg added">Added note · verify</span></div>')
    views.append(f'<div class="taxv" id="tax-home" hidden><div class="bar"><button type="button" class="back" data-home>← Home</button></div>'
                 f'<p class="crumb">Taxation</p><h2>Taxation Handouts</h2>'
                 f'<p class="intro">Every tax problem is three questions: <b>who</b> is the taxpayer, <b>what kind</b> of income or transaction it is, and <b>what rate</b> applies and when. '
                 f'Start with {link("start", "Start Here")}, then use the rates, hooks and quiz daily. Links inside the notes open the related chapter; tap <b>↩ Back</b> to return to where you were.</p>'
                 + legend + "".join(groups_html) + '</div>')
    # pages
    for idx, (sheet, slug, name, desc) in enumerate(ORDER):
        blocks = pages[sheet]
        title = title_fix([b["text"] for b in blocks if b["kind"] == "title"][0])
        if slug == "quiz":
            body, toc = render_quiz(blocks), []
        elif slug == "calc":
            body, toc = render_calc(blocks), []
        else:
            body, toc = render_blocks(blocks, slug)
        sub = f'<p class="psub">{fmt(title, links=False)}</p>' if slug not in ("quiz", "calc") and title.upper().replace("'", "") != name.upper().replace("'", "") else ""
        chips = ('<nav class="otp"><span>On this page:</span>' + "".join(f'<a class="jump" href="#tax-{slug}--{k}">{fmt(t, links=False).capitalize() if t.isupper() else fmt(t, links=False)}</a>' for k, t in toc) + "</nav>") if len(toc) > 1 else ""
        prev_ = ORDER[idx - 1] if idx > 0 else None
        next_ = ORDER[idx + 1] if idx + 1 < len(ORDER) else None
        pn = ('<nav class="pn">' + (f'<a class="xl" href="#tax-{prev_[1]}">← {prev_[2]}</a>' if prev_ else "<span></span>")
              + (f'<a class="xl nx" href="#tax-{next_[1]}">{next_[2]} →</a>' if next_ else "") + "</nav>")
        views.append(f'<div class="taxv ho" id="tax-{slug}" hidden><div class="bar"><button type="button" class="back" data-back>← Back</button>'
                     f'<a class="tab xl" href="#tax">Contents</a></div><p class="crumb">Taxation · {idx + 1} of {len(ORDER)}</p>'
                     f'<h2>{name}</h2>{sub}{chips}{body}{pn}</div>')
    box = ('<a class="sec xl" href="#tax"><b>Taxation</b>Income tax, transfer taxes, VAT and business taxes, local taxes, remedies, law updates'
           f'<small>{len(ORDER)} chapters · Rates · Hooks · 119-question quiz · Calculators</small></a>')
    return box, "".join(views)

CSS = """
a.xl{color:var(--deep);font-weight:bold;text-decoration:underline;text-decoration-color:var(--line);text-underline-offset:3px}
a.sec.xl{text-decoration:none;font-weight:normal}
.subj{font-size:14px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin:26px 0 10px}
.subj:first-of-type{margin-top:0}
.toclist{list-style:none;padding:0;margin:0 0 8px;display:flex;flex-direction:column;gap:8px}
a.toc{display:grid;grid-template-columns:1fr auto;gap:2px 10px;padding:12px 14px;border:1px solid var(--line);border-radius:10px;background:var(--soft);text-decoration:none;color:var(--ink);font-weight:normal}
a.toc:hover{border-color:var(--rose)}
.tn{font-weight:bold;color:var(--deep)} .td{grid-column:1;color:var(--muted);font-size:.9em}
.pr{grid-column:2;grid-row:1/span 2;align-self:center;font-size:12px;font-weight:bold;border-radius:999px;padding:3px 10px}
.p3{background:var(--rose);color:#ffffff} .p2{background:var(--pink);color:var(--deep)} .p1{background:#f1edef;color:var(--muted)}
.taxv h3{font-size:19px;color:var(--deep);margin:26px 0 8px;padding-bottom:4px;border-bottom:2px solid var(--pink);scroll-margin-top:16px}
.psub{color:var(--muted);margin:-4px 0 12px}
.big{background:#fff8e1;border:1px solid #f0dca0;border-radius:10px;padding:12px 14px;margin:10px 0 14px}
.lbl{display:block;font-size:12px;font-weight:bold;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;color:var(--muted)}
.band{border-radius:10px;padding:12px 14px;margin:12px 0;border-left:5px solid}
.band.hook,.lg.hook{background:#e9f5e1;border-color:#5f9b3d}
.band.trap,.lg.trap{background:#fde8e4;border-color:#c0392b}
.band.added,.lg.added{background:#e6f0fb;border-color:#3d6fb4}
.five,.lg.five{background:#fff6d6;border:1px solid #edd27a}
.five{border-radius:10px;padding:12px 14px;margin:16px 0}
.five ol{margin:0;padding-left:22px}
.hook .lbl{color:#3f6f25} .trap .lbl{color:#a32a1e} .added .lbl{color:#2f5a96} .five .lbl{color:#8a6a00}
.legend{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 8px;font-size:14px}
.lg{border-radius:6px;padding:2px 10px;border-left:4px solid}
.lg.five{border-left:4px solid #edd27a}
strong.mem{color:#b0122b}
.added-t{color:#2f5a96}
.note{color:var(--muted);font-size:.95em}
ul.bl{padding-left:22px} ul.bl li{margin-bottom:6px}
table.tx td{text-align:left;vertical-align:top} table.tx th{text-align:left}
.otp{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:4px 0 14px;font-size:14px}
.otp span{color:var(--muted);margin-right:2px}
a.jump{border:1px solid var(--line);border-radius:999px;padding:4px 10px;text-decoration:none;color:var(--deep);background:var(--bg)}
.pn{display:flex;justify-content:space-between;gap:12px;margin-top:30px;padding-top:14px;border-top:2px solid var(--pink)}
.pn a{text-decoration:none}
a.tab.xl{text-decoration:none}
.filter{display:flex;gap:8px;align-items:center;margin:0 0 14px;font-weight:bold;color:var(--deep)}
.filter select{font:inherit;padding:6px 8px;border:1.5px solid var(--rose);border-radius:8px;background:var(--bg);color:var(--ink);max-width:100%}
.tq .tag a{font-weight:bold}
.calc{background:var(--soft);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin-bottom:16px}
.calc h3{margin-top:0}
.calcfx{background:var(--bg);margin:0 0 14px}
.calcfx .lbl{color:var(--deep)}
.dn{background:#e6f0fb;border-left:4px solid #3d6fb4;border-radius:0 8px 8px 0;padding:10px 14px;margin:0 0 14px;display:flex;flex-direction:column;gap:6px}
.dn .lbl{color:#2f5a96}
.cf{display:flex;flex-direction:column;gap:4px;margin-bottom:10px}
.cf span{font-size:.92em}
.cf input{font:inherit;padding:8px 10px;border:1.5px solid var(--line);border-radius:8px;background:#fffdf3;color:#1f4e9e;max-width:100%}
.cf input:focus{outline:2px solid var(--rose);border-color:var(--rose)}
.out{display:flex;flex-direction:column;gap:4px;margin-top:6px}
.calc{position:relative}
.out .row{position:relative;display:grid;grid-template-columns:1fr auto auto;align-items:center;gap:4px 10px;border-bottom:1px dashed var(--line);padding:4px 0;font-variant-numeric:tabular-nums}
.out .row b{text-align:right}
.out .row:has(.wk) > b{cursor:pointer;text-decoration:underline dotted var(--rose);text-underline-offset:4px}
.wk{width:30px;height:30px;border-radius:50%;border:1.5px solid var(--rose);background:var(--bg);color:var(--deep);font-weight:bold;font-size:16px;line-height:1;padding:0}
.wk[aria-expanded="true"]{background:var(--rose);color:#ffffff}
.work{grid-column:1/-1;justify-self:end;width:100%;max-width:100%;background:var(--bg);border:1.5px solid var(--rose);border-radius:10px;padding:10px 12px;margin:6px 0 4px;box-shadow:0 4px 12px rgba(120,30,60,.12);font-variant-numeric:tabular-nums;position:relative}
.work::before{content:"";position:absolute;top:-8px;right:8px;width:12px;height:12px;background:var(--bg);border-left:1.5px solid var(--rose);border-top:1.5px solid var(--rose);transform:rotate(45deg)}
.work div{padding:1px 0}
.work .lbl{color:var(--deep)}
.out .res{border-bottom:0;background:var(--pink);border-radius:8px;padding:8px 10px;margin-top:4px}
.out .res .work{margin-bottom:2px}
.calc-l{font-size:.9em;margin:8px 0 0}
#retpill{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:20;background:var(--deep);color:#ffffff;border:0;border-radius:999px;padding:12px 20px;font-size:16px;font-weight:bold;box-shadow:0 4px 14px rgba(120,30,60,.35);max-width:calc(100% - 32px);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hit{background:#fff3b0!important;transition:background .8s}
@media (max-width:600px){
 table.tx.st,table.tx.st tbody,table.tx.st tr,table.tx.st td{display:block;width:100%}
 table.tx.st{min-width:0} table.tx.st thead{display:none}
 table.tx.st tr{border:1px solid var(--line);border-radius:10px;margin-bottom:10px;padding:6px 10px;background:var(--bg)}
 table.tx.st td{border:0;padding:4px 0}
 table.tx.st td[data-label]::before{content:attr(data-label);display:block;font-size:13px;font-weight:bold;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
 .taxv h3{font-size:21px} .otp{font-size:15px} a.jump{padding:6px 12px}
 .pr{font-size:13px}
}
"""

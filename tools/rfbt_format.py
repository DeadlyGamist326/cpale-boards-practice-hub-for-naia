"""Formats flashcard answers for display: enumerations become lists, key words and figures become bold.
Markup is produced as safe HTML from escaped text."""
import html, re
from rfbt_ask import ask, STEM
from rfbt_keys import KEYS

# Hand-written layouts for cards whose automatic split is not good enough.
# Syntax: lines; "- " = bullet, "1. " = numbered; **bold**.
OVERRIDES = {
 "Dependents' pension":
   "**10%** of the monthly pension or **₱250**, **whichever is higher**, per dependent child:\n- Conceived **on or before** the contingency\n- **Up to 5 children**\n- Starting with the **youngest**\n- **Without substitution**\n- **Legitimate** children are preferred",
 "Sickness benefit eligibility":
   "1. At least **3 monthly contributions** in the **12 months** before the semester of sickness or injury\n2. Confined for **MORE than 3 days** in a hospital or elsewhere with SSS approval",
 "Limits on the sickness benefit":
   "- **120 days** per calendar year (unused days do **not** carry over)\n- **240 days** for the **same confinement**",
 "Holiday pay for an unworked regular holiday":
   "At least **100%** of the daily wage, provided the employee is:\n- **Present**, or\n- On **paid leave**\non the workday **immediately before** the holiday",
 "Paternity leave":
   "- **7 days** with **full pay**\n- For the **first 4 deliveries**\n- Of the **legitimate spouse**\n- With whom the married male employee is **cohabiting**",
 "Parental leave for solo parents":
   "- **Not more than 7 working days** with pay every year\n- **Forfeitable** and **non-cumulative**\n- For a solo parent with at least **6 months** of service",
 "Who are entitled to 13th month pay?":
   "- **All rank-and-file** employees\n- Regardless of the nature of employment or how paid\n- Who worked at least **1 month** in the calendar year",
 "Compensation under RA 11199":
   "All actual remuneration for employment, **including**:\n- The mandated **COLA**\n- The **cash value** of non-cash pay\n**Except** the part received during the month **in excess of the maximum salary credit**",
 "Employer under RA 11199":
   "Any person, natural or juridical, domestic or foreign, who:\n- Carries on in the Philippines any trade, business, industry, undertaking or activity, and\n- Uses the services of another **under his orders**\n**Except** the **Government** and its political subdivisions, branches, instrumentalities and **GOCCs**",
 "Who is the Vice-Chairperson of the Social Security Commission?":
   "The **SSS President and CEO**; acts as Chairperson when the **Finance Secretary is absent**",
 "Declaration of basic policy of the Labor Code":
   "The State shall:\n1. Afford **protection to labor**\n2. Promote **full employment**\n3. Ensure **equal work opportunities** regardless of sex, race or creed\n4. **Regulate the relations** between workers and employers",
 "Labor standards":
   "The **minimum requirements** prescribed by laws and rules on:\n- Wages\n- Hours of work\n- COLA\n- Other monetary and welfare benefits\n- **Occupational safety and health** standards",
 "Two successive regular holidays (e.g., Maundy Thursday and Good Friday): an employee absent the day before the first holiday is paid ___.":
   "**Not** for both holidays.\n**Unless** he or she **works on the first holiday**: then he or she gets holiday pay on the **second**",
 "Within how many days must the employee notify the employer of sickness?":
   "**5 calendar days** after confinement starts.\n**Not needed** if:\n- Confined in a **hospital**, or\n- Sick or injured **while working** or **on the employer's premises**",

 "Additional benefit allowance for pensioners (from January 2017)":
   "**₱1,000 a month** for:\n- retirement\n- death\n- disability pensioners\nSeparate from the pension; it **does not cover** the dependents' pension",
 "Monthly pension: the highest of what three amounts?":
   "The **highest** of:\n1. **₱300** + **20%** of AMSC + **2%** of AMSC for each credited year of service beyond **10**\n2. **40%** of AMSC\n3. **₱1,000**\nPaid for **no less than 60 months** in total.",
 "Composition of the Social Security Commission (9 members)":
   "**9 members:**\n- **Secretary of Finance** (Chairperson)\n- **SSS President and CEO** (Vice-Chairperson)\n- **Secretary of Labor** (ex officio)\n- **6 appointive members:** 3 for workers, 3 for employers; each group with **at least 1 woman**",
 "Average monthly salary credit (AMSC)":
   "The **higher** of:\n1. Sum of the **last 60 MSCs** before the semester of contingency **÷ 60**\n2. Sum of **all MSCs paid** before the semester **÷ number of monthly contributions paid**",
 "Death benefit when the member paid FEWER than 36 monthly contributions":
   "**Lump sum** to primary or secondary beneficiaries, the **higher** of:\n1. Monthly pension **×** number of contributions paid\n2. **12 ×** the monthly pension",
 "Permanent total disability benefit with FEWER than 36 contributions":
   "**Lump sum**, the **higher** of:\n1. Monthly pension **×** number of contributions paid\n2. **12 ×** the monthly pension",
 "Overtime rates: rest or special day / special day on rest day / regular holiday / regular holiday on rest day":
   "- Rest or special day: **169%**\n- Special day on rest day: **195%**\n- Regular holiday: **260%**\n- Regular holiday on rest day: **338%**\nof the hourly rate",
 "Night shift rates: ordinary day / rest or special day / regular holiday / regular holiday on rest day":
   "- Ordinary day: **110%**\n- Rest or special day: **143%**\n- Regular holiday: **220%**\n- Regular holiday on rest day: **286%**\nof the hourly rate",
 "Double holiday rates: unworked-and-worked / on rest day / overtime":
   "- Double holiday (worked): **300%**\n- On rest day: **390%**\n- Overtime: **390%** (3 × 1.3)",
 "Double regular holiday: pay if unworked / if worked":
   "- Unworked: **200%**\n- Worked: **300%**\nof the daily wage",
 "Permanent partial disability (after 36 contributions): months of pension for loss of one hand / one arm / one foot / one leg":
   "- One hand: **39 months**\n- One arm: **50 months**\n- One foot: **31 months**\n- One leg: **46 months**",
 "Permanent partial disability: months of pension for one thumb / one index finger / one big toe / sight of one eye":
   "- One thumb: **10 months**\n- One index finger: **8 months**\n- One big toe: **6 months**\n- Sight of one eye: **25 months**",
 "Permanent partial disability: months of pension for hearing of one ear / hearing of both ears / both ears":
   "- Hearing of one ear: **10 months**\n- Hearing of both ears: **50 months**\n- Both ears: **20 months**",
 "When are National Heroes Day and Araw ng Kagitingan observed?":
   "- National Heroes Day: **last Monday of August**\n- Araw ng Kagitingan: **Monday nearest April 9**",
 "When does compulsory coverage take effect for the employer? For the employee?":
   "- Employer: **first day of operation**\n- Employee: **the day of employment**",
 "Who are the dependents of a member?":
   "1. **Legal spouse** entitled by law to support\n2. **Legitimate, legitimated, legally adopted, and illegitimate child** who is unmarried, not gainfully employed, and **below 21**\n3. **Parent** receiving regular support from the member",
 "Factors for converting a daily wage to an annual amount":
   "- **365** for monthly-paid employees\n- **313** for daily-paid employees not paid on rest days",
 "The regular holidays":
   "1. New Year's Day\n2. Maundy Thursday\n3. Good Friday\n4. Eidul Fitr\n5. Eidul Adha\n6. Araw ng Kagitingan\n7. Labor Day\n8. Independence Day\n9. National Heroes Day\n10. Bonifacio Day\n11. Christmas Day\n12. Rizal Day",
 "The regular special (non-working) days":
   "- Ninoy Aquino Day: **Aug 21**\n- All Saints' Day: **Nov 1**\n- Feast of the Immaculate Conception: **Dec 8**\n- Last Day of the Year: **Dec 31**",
 "Days traditionally declared as additional special (non-working) days":
   "- Chinese New Year\n- Black Saturday\n- All Souls' Day: **Nov 2**\n- Christmas Eve: **Dec 24**",
 "Examples of involuntary separation":
   "- Installation of labor-saving devices\n- Redundancy\n- Retrenchment to prevent loss\n- Closure or cessation of operation\n- Disease or illness",
 "Primary beneficiaries":
   "- The **dependent spouse** until he or she **remarries**\n- The **dependent legitimate, legitimated, legally adopted, and illegitimate children**",
 "SSS benefit payments are exempt from ___.":
   "- **All taxes, fees or charges**\n- **Attachment, garnishment, levy or seizure**\n**Except** to pay the member's debt to the SSS",
 "What is EXCLUDED from basic salary for the 13th month pay?":
   "- Cash equivalent of unused **vacation and sick leave**\n- **Overtime**\n- **Premium** pay\n- **Night shift differential**\n- **Holiday pay**\n- **COLA**\nUnless treated as part of basic salary by agreement, practice or policy",
 "Who are covered by the Expanded Maternity Leave Law?":
   "Female workers, regardless of civil status, employment status, or the child's legitimacy:\n- **Public sector**\n- **Private sector**\n- **Informal economy**\n- **Voluntary SSS contributors**\n- **National athletes**",
 "If the father is dead, absent, or incapacitated, the mother may allocate leave to ___.":
   "An **alternate caregiver**:\n- A **relative within the 4th degree** of consanguinity, or\n- Her **current partner** sharing the household, regardless of sexual orientation or gender identity",
 "When are the disability pension and dependents' pension suspended?":
   "- **Reemployment** or resumption of self-employment\n- **Recovery** from the disability\n- **Failure to appear** for examination at least **once a year** when notified",
 "Conditions for maternity leave":
   "1. At least **3 monthly SSS contributions** in the **12 months** before the semester of childbirth, miscarriage or emergency termination\n2. **Notice** to the employer (or SSS) of the pregnancy and probable delivery date",
 "How are unpaid contributions collected when an employer refuses or neglects to pay?":
   "- In the same manner as **taxes under the NIRC**\n- By **court action**\n- By a **warrant to the sheriff** to levy and sell the debtor's property",
 "Unemployment insurance (involuntary separation) benefit":
   "**50% of AMSC** monthly for up to **2 months**, claimable **once every 3 years**.\nRequirements:\n- Member **not over 60**\n- At least **36 monthly contributions**, **12** of them in the **18 months** before separation",
 "Who qualifies for the retirement pension?":
   "A member with at least **120 monthly contributions** before the semester of retirement who is:\n- **60** and separated from employment (or no longer self-employed), or\n- **65**",
 "Maternity leave for live childbirth":
   "- **105 days with full pay**\n- **+15 days** with full pay for a **solo parent**\n- Optional extra **30 days WITHOUT pay**, with due notice to the employer",
}

EMPH = [
    r"₱\d{1,3}(?:,\d{3})*(?:\.\d+)?(?:\s(?:to|and)\s₱\d{1,3}(?:,\d{3})*(?:\.\d+)?)?",
    r"\b\d+(?:\.\d+)?%",
    r"\b\d+(?:,\d{3})*(?:\.\d+)?\s(?:calendar\s|working\s|consecutive\s|monthly\s)?(?:days?|years?|months?|hours?|weeks?|minutes|workers|employees|children|contributions|times|members|pairs)\b",
    r"\b(?:\d+(?:st|nd|rd|th))\s(?:degree|week)\b",
    r"\b(?:NOT|EXCEPT|ONLY|FEWER|MORE|ALL|BOTH|WITHOUT|HIGHER)\b",
    r"\b(?:No|None|Not|Yes)\b(?=[.,]|\s)",
    r"\bwhichever is higher\b", r"\bthe higher of\b", r"\bin favor of labor\b",
    r"\b(?:10:00 PM|6:00 AM|5:00 AM|midnight)\b",
    r"\b(?:December 24|January)\b",
]
EMPH_RE = re.compile("|".join(f"(?:{p})" for p in EMPH))

def _inline(t):
    t = html.escape(t, quote=False)
    if "**" in t:
        return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return EMPH_RE.sub(lambda m: f"<b>{m.group(0)}</b>", t)

def _from_lines(lines):
    out, lst, sub = [], None, False
    for ln in lines:
        ms = re.match(r"^\s{2,}- (.*)$", ln)
        if ms and lst:
            if not sub:
                out[-1] = out[-1][:-5] if out[-1].endswith("</li>") else out[-1]
                out.append('<ul class="sub">'); sub = True
            it = ms.group(1); out.append(f"<li>{_inline(it[:1].upper() + it[1:])}</li>"); continue
        if sub:
            out.append("</ul></li>"); sub = False
        m = re.match(r"^(?:- |(\d+)\. )(.*)$", ln)
        if m:
            kind = "ol" if m.group(1) else "ul"
            if lst != kind:
                if lst: out.append(f"</{lst}>")
                out.append(f"<{kind}>"); lst = kind
            item = re.sub(r"^\([a-z]\)\s*", "", m.group(2))
            item = item[:1].upper() + item[1:]
            out.append(f"<li>{_inline(item)}</li>")
        else:
            if lst: out.append(f"</{lst}>"); lst = None
            out.append(f"<p>{_inline(ln)}</p>")
    if sub: out.append("</ul></li>")
    if lst: out.append(f"</{lst}>")
    return "".join(out)

def auto_lines(a):
    # (1) ... (2) ... enumerations
    if re.search(r"\(1\)", a) and re.search(r"\(2\)", a):
        head, _, rest = a.partition("(1)")
        items = [x.strip(" ;,.") for x in re.split(r"\(\d\)", "(1)" + rest)[1:]]
        tail = ""
        last = items[-1]
        m = re.search(r"\.\s+(?=[A-Z])", last)
        if m: items[-1], tail = last[:m.start()], last[m.end():]
        lines = ([head.strip(" :;")] if head.strip(" :;") else []) + [f"{n}. {x}" for n, x in enumerate(items, 1)]
        return lines + ([tail] if tail else [])
    # intro: a; b; c  -> bullets
    parts = [p.strip() for p in re.split(r";\s+(?![^()]*\))", a)]
    if len(parts) >= 3 or (len(parts) == 2 and all(len(p) < 90 for p in parts) and len(a) > 70):
        head = ""
        m = re.match(r"^(.{3,80}?):\s+(.*)$", parts[0])
        if m: head, parts[0] = m.group(1) + ":", m.group(2)
        last = parts[-1]
        tail = ""
        m2 = re.search(r"\.\s+(?=(?:Also|Not|Paid|Separate|If|The|It|This|Choose|Only|Needs?|For)\b)", last)
        if m2: parts[-1], tail = last[:m2.start()], last[m2.end():]
        lines = ([head] if head else []) + ["- " + p.rstrip(".").removeprefix("and ").removeprefix("or ") for p in parts]
        return lines + ([tail] if tail else [])
    # comma enumerations after a colon: "X: a, b, c, d"
    m = re.match(r"^(.{3,80}?):\s+(.*)$", a)
    if m and m.group(2).count(",") >= 3 and len(m.group(2)) < 260:
        items = [x.strip() for x in re.split(r",\s+(?:and\s+|or\s+)?(?![^()]*\))", m.group(2).rstrip("."))]
        return [m.group(1) + ":"] + ["- " + x for x in items]
    # plain sentences on separate lines
    sents = re.split(r"(?<=[.)])\s+(?=[A-Z])", a)
    return sents

# user request: no ALL-CAPS emphasis; bold + color is enough. Acronyms (SSS, COLA, RA...) stay.
DECAP = "AND ARE DAY DIFFERENTIAL EXCEPT EXCLUDED FEWER FIVE HOLIDAY MORE NIGHT NOT ON OR PAY PREMIUM SHIFT THAT TOTAL WITHOUT ONLY BOTH ALL HIGHER".split()
DECAP_RE = re.compile(r"\b(?:" + "|".join(DECAP) + r")\b")

def decap(h):
    """Lower-case emphasis caps in the text of an HTML string (sentence starts keep a capital)."""
    out, start = [], True
    for tok in re.split(r"(<[^>]+>)", h):
        if tok.startswith("<"):
            if re.match(r"<(?:li|p)[\s>]", tok) or tok.startswith('<span class="stem"'): start = True
            out.append(tok); continue
        def sub(m, tok=tok, start=start):
            w = m.group(0).lower()
            before = tok[:m.start()].rstrip()
            if (start and not before) or before.endswith((".", "?", "!")):
                w = w.capitalize()
            return w
        out.append(DECAP_RE.sub(sub, tok))
        if tok.strip(): start = False
    return "".join(out)

def keymark(h, front, open_tag):
    """Bold the card's KEYS phrases in text outside existing <b> tags."""
    ph = [p for p in KEYS.get(front, "").split("|") if p]
    if not ph:
        return h
    rx = re.compile(r"(?<!\w)(?:" + "|".join(re.escape(html.escape(p, quote=False)) for p in sorted(ph, key=len, reverse=True)) + r")(?!\w)", re.I)
    out, depth = [], 0
    for tok in re.split(r"(<[^>]+>)", h):
        if tok.startswith("<"):
            if re.match(r"<b[\s>]", tok): depth += 1
            elif tok == "</b>": depth -= 1
            out.append(tok)
        elif depth == 0:
            out.append(rx.sub(lambda m: open_tag + m.group(0) + "</b>", tok))
        else:
            out.append(tok)
    return "".join(out)

def fmt(front, a):
    src = OVERRIDES.get(front)
    lines = src.split("\n") if src else auto_lines(a)
    if front in STEM:
        assert src and lines[0].rstrip().endswith(":"), front
        lines = lines[1:]
    big = (not src) and len(lines) == 1 and len(a) <= 45
    return big, decap(_from_lines(lines) if big else keymark(_from_lines(lines), front, "<b>"))

# ---- question side ----
TERMS = sorted(r"""Social Security Act of 2018|Social Security Commission|SSS|Commission|Chairperson|Vice-Chairperson|appointive|term of office|
employer|employee|self-employed|employment|dependents?|dependent child|primary beneficiaries|secondary beneficiaries|beneficiaries|illegitimate children|legitimate children|
compensation|monthly salary credit|average monthly salary credit|average daily salary credit|AMSC|ADSC|semester|quarter|credited years of service|contingency|contingencies|
compulsory coverage|coverage|voluntary|kasambahays?|household helpers|OFWs?|sea-based|land-based|manning agency|manning agencies|permanent migrants|
Annual Register|business permit|contributions?|remit|late remittance|penalty|prescriptive period|exempt|
monthly pension|minimum monthly pension|additional benefit allowance|dependents' pension|retirement pension|retiree|retirement|lump sum|death benefit|
permanent total disability|permanent partial disability|disability pension|disability|funeral benefit|sickness benefit|sickness allowance|sickness benefit|sickness|
unemployment insurance|involuntary separation|compensable contingencies|misappropriates|false statements|
Labor Code|Presidential Decree|basic policy|in favor of labor|diminution of benefits|labor standards|wage|salary|basic pay|basic salary|wage order|
regional minimum wage|collective bargaining|BMBEs?|holiday pay|regular holidays?|double regular holiday|special \(non-working\) days?|premium pay|rest day|weekly rest day|
managerial employee|managerial staff|field personnel|National Heroes Day|Araw ng Kagitingan|leave WITHOUT pay|successive regular holidays|
normal hours of work|hours worked|meal period|undertime|overtime|compulsory overtime|night shift differential|night shift|hourly rate|
13th month pay|PD 851|service incentive leave|vacation and sick leaves|maternity leave|postnatal leave|emergency termination of pregnancy|miscarriage|
Expanded Maternity Leave Law|child's father|alternate caregiver|paternity leave|cohabiting|solo parents?|parental leave|daily wage|hazards|independent contractors?|spouses|managing the household|at least one year of service|father is dead""".replace("\n", "").split("|"), key=len, reverse=True)
TERM_RE = re.compile(r"(?<![\w-])(?:" + "|".join(TERMS) + r")(?![\w-])", re.I)
CAPS_RE = re.compile(r"\b(?:NOT|EXCEPT|ONLY|FEWER|MORE|EXCLUDED|BOTH|TOTAL|WITHOUT|THIS|HIGHER|ORGANIZED|UNORGANIZED|SIZE|PENSION|MONTHLY|FIRST)\b")
NUM_RE = re.compile(r"₱\d{1,3}(?:,\d{3})*|\b\d+(?:\.\d+)?%|\b\d+(?:st|nd|rd|th)?\b(?:\s(?:days?|years?|months?|hours?|contributions|monthly contributions|deliveries))?")

def qfmt(front):
    t = html.escape(ask(front), quote=False)
    marks = []
    for rx, cls in ((CAPS_RE, "k"), (TERM_RE, "t"), (NUM_RE, "k")):
        for m in rx.finditer(t):
            if any(not (m.end() <= a or m.start() >= b) for a, b, _ in marks): continue
            marks.append((m.start(), m.end(), cls))
    out, pos = [], 0
    for a, b, cls in sorted(marks):
        out.append(t[pos:a]); out.append(f'<b class="{cls}">{t[a:b]}</b>'); pos = b
    out.append(t[pos:])
    s = "".join(out).replace("___", '<span class="blank">_____</span>')
    s = keymark(s, front, '<b class="t">')
    if "\n" in s:
        a, b = s.split("\n", 1)
        s = a + '<span class="stem">' + b + '</span>'

    return decap(s)

# ---- comma lists turned into bullets (user request: enumerate wherever possible) ----
OVERRIDES.update({
 "The hazards social security protects members against": """- **Disability**
- **Sickness**
- **Maternity**
- **Old age**
- **Death**
- Other contingencies resulting in **loss of income** or **financial burden**""",
 "The SSS functions and operates as what kind of entity?": """- **Independent** and **accountable**
- **Government-owned and -controlled corporation (GOCC)**
- Principal place of business: **Metro Manila**""",
 "Composition of the Social Security Commission (9 members)": """**9 members:**
- **Secretary of Finance** (Chairperson)
- **SSS President and CEO** (Vice-Chairperson)
- **Secretary of Labor** (ex officio)
- **6 appointive members:**
  - **3** for workers
  - **3** for employers
  - Each group with **at least 1 woman**""",
 "Who are the dependents of a member?": """1. **Legal spouse** entitled by law to support
2. **Legitimate, legitimated, legally adopted, and illegitimate child** who is:
  - **Unmarried**
  - **Not gainfully employed**
  - **Below 21**
3. **Parent** receiving regular support from the member""",
 "A child over 21 is still a dependent if ___.": """He or she, **congenitally** or **while still a minor**, became:
- **Permanently incapacitated**
- **Incapable of self-support**, physically or mentally""",
 "Monthly salary credit": """- The **compensation base** for **contributions and benefits**
- For computing benefits, the **maximum MSC** is **₱20,000** until adjusted""",
 "Primary beneficiaries": """- The **dependent spouse** until he or she **remarries**
- The **dependent children**:
  - **Legitimate**
  - **Legitimated**
  - **Legally adopted**
  - **Illegitimate**""",
 "Contingencies under RA 11199": """- **Retirement**
- **Death**
- **Disability**
- **Injury or sickness**
- **Maternity**
- The IRR adds **unemployment or involuntary separation**""",
 "Quarter": """**Three consecutive calendar months** ending on the last day of:
- **March**
- **June**
- **September**
- **December**""",
 "Whose contributions does a self-employed member pay?": """- **Both** the **employer** and the **employee** contributions
- Based on the **monthly earnings declared** at registration""",
 "Before issuing an annual business permit, an LGU must require ___.": """- A **certificate of SSS coverage and compliance**
- The SSS must issue it within **5 working days**""",
 "SSS benefit payments are exempt from ___.": """- **All taxes, fees or charges**
- **Attachment**
- **Garnishment**
- **Levy**
- **Seizure**
**Except** to pay the member's debt to the SSS""",
 "A member who is 60 at retirement but lacks 120 contributions gets ___.": """A **lump sum** equal to the **total contributions paid** by and for him, if:
- **Separated** from employment
- **Not continuing** to pay""",
 "Funeral benefit under RA 11199": """- **₱12,000**, in **cash or in kind**
- The IRR now sets a **variable ₱20,000 to ₱40,000**, effective August 1, 2015""",
 "Penalty for failing to register employees or to deduct and remit contributions": """**Both:**
- **Fine** of **₱5,000 to ₱20,000**
- **Imprisonment** of **6 years and 1 day to 12 years**""",
 "Besides money, wage also includes ___.": """The **fair and reasonable value** of:
- **Board**
- **Lodging**
- **Other facilities** customarily furnished by the employer
Value is determined by the **Secretary of Labor**, and must **not include any profit** to the employer.""",
 "Basic pay (basic salary)": """- The **rate of pay** for a **standard work period**
- **Excluding** additional payments such as **bonuses** and **overtime**""",
 "Special (non-working) day, unworked": """**"No work, no pay"**, unless pay is granted by a favorable:
- **Company policy**
- **Practice**
- **CBA**""",
 "\"At least one year of service\" means ___.": """**At least 12 months** from the start of work:
- **Continuous or broken**
- **Including** authorized absences and paid regular holidays
- Or a **shorter period** if that is the company's working year""",
 "What happens to unused service incentive leave?": """- **Commuted to cash** at the **end of the year**
- If never used or commuted: paid upon **resignation or separation**
- At the **salary rate on the date of commutation**""",
 "Are vacation and sick leaves mandated by law?": """**No.** The law mandates only the **5-day service incentive leave**, usable for:
- **Sick** leave
- **Vacation** leave
- **Other purposes**""",
})

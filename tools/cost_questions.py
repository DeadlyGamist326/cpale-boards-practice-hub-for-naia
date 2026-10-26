"""Cost Concepts & Cost Behavior: 20 problems (two versions of each of 10 problem types).
Every answer, distractor and solution line is computed from the givens."""
import random
from cvp_questions import P, num, tbl, part

def K(x): return P(x * 1000)  # givens below are written in thousands

Q = []

# 1: prime and conversion cost
def t1(intro, beg, end, purch, dl, oh, q1, q2):
    used = beg + purch - end; prime = used + dl; conv = dl + oh
    t = tbl([["Direct materials purchased", K(purch)], ["Direct labor", K(dl)], ["Factory overhead", K(oh)]])
    s0 = f"Direct materials used = Beginning + Purchases − Ending = {K(beg)} + {K(purch)} − {K(end)} = {K(used)}"
    return dict(topic="Prime and conversion cost", stem=intro + t, parts=[
        part(q1, K(prime), [K(purch + dl), K(used + oh), K(conv)],
             [s0, f"Prime cost = Direct materials used + Direct labor = {K(used)} + {K(dl)} = {K(prime)}"]),
        part(q2, K(conv), [K(oh), K(prime), K(used + oh)],
             [f"Conversion cost = Direct labor + Factory overhead = {K(dl)} + {K(oh)} = {K(conv)}"])])

# 2: work back to direct materials
def t2a(stem, prime, oh, dl):
    dm = prime - dl
    return dict(topic="Working back: direct materials", stem=stem, parts=[part("", K(dm),
        [K(prime - oh), K(prime - dl - oh), K(dl + oh)],
        ["Prime cost = Direct materials + Direct labor", f"Direct materials = {K(prime)} − {K(dl)} = {K(dm)}",
         "Overhead is not part of prime cost, so it is not needed."])])
def t2b(stem, conv, oh, prime):
    dl = conv - oh; dm = prime - dl
    return dict(topic="Working back: direct materials", stem=stem, parts=[part("", K(dm),
        [K(prime - oh), K(dl), K(conv - prime + oh)],
        [f"Direct labor = Conversion cost − Overhead = {K(conv)} − {K(oh)} = {K(dl)}",
         f"Direct materials = Prime cost − Direct labor = {K(prime)} − {K(dl)} = {K(dm)}"])])

# 3: product costs
def t3(stem, dm, dl, oh, others):
    pc = dm + dl + oh; allc = pc + sum(others)
    return dict(topic="Product costs", stem=stem, parts=[part("", K(pc), [K(dm + dl), K(dl + oh), K(allc)],
        [f"Product costs = Direct materials + Direct labor + Manufacturing overhead",
         f"= {K(dm)} + {K(dl)} + {K(oh)} = {K(pc)}",
         "Selling and administrative expenses are period costs, so they are excluded."])])

# 4: period costs
def t4(stem, items, wrong):
    per = [(n, v) for n, v, is_per in items if is_per]
    tot = sum(v for _, v in per)
    return dict(topic="Period costs", stem=stem, parts=[part("", K(tot), [K(w) for w in wrong],
        ["Period costs are selling and administrative costs, expensed when incurred.",
         "Period costs = " + " + ".join(f"{K(v)} ({n})" for n, v in per) + f" = {K(tot)}",
         "Factory costs (" + ", ".join(n for n, v, p in items if not p) + ") are product costs."])])

# 5: mixed cost at a new volume
def t5(stem, u1, tc, vc_or_fc, is_vc, u2):
    vc = vc_or_fc if is_vc else tc - vc_or_fc
    fc = tc - vc; vu = vc / u1; new = fc + vu * u2
    s = [f"Fixed costs = {K(tc)} − {K(vc)} = {K(fc)}" if is_vc else f"Variable costs = {K(tc)} − {K(fc)} = {K(vc)}",
         f"Variable cost per unit = {K(vc)} ÷ {num(u1 * 1000)} = {P(vu, 2)}",
         f"Total cost at {num(u2 * 1000)} units = {K(fc)} + {P(vu, 2)} × {num(u2 * 1000)} = {K(fc)} + {K(vu * u2)} = {K(new)}",
         "Fixed costs stay the same in total; only variable costs change with volume."]
    return dict(topic="Cost behavior: mixed costs", stem=stem, parts=[part("", K(new),
        [K(tc * u2 / u1), K(vu * u2), K(tc)], s)])

# 6: classify a cost list
def t6(intro, items, qs):
    # items: (name, amount, kind) kind in DM DL OH PER
    tot = lambda k: sum(v for _, v, kk in items if kk in k)
    oh, dm, dl, per = tot("OH"), tot("DM"), tot("DL"), tot("PER")
    allc = oh + dm + dl + per
    rows = [[n, K(v)] for n, v, _ in items]
    names = lambda k: " + ".join(f"{n} {K(v)}" for n, v, kk in items if kk == k)
    ohn = [n for n, v, k in items if k == "OH"]
    return dict(topic="Classifying costs", stem=intro + tbl(rows), parts=[
        part(qs[0], K(oh), [K(oh - items[[n for n, _, _ in items].index(ohn[-1])][1]), K(dm + dl), K(allc)],
             [f"Manufacturing overhead = {names('OH')} = {K(oh)}",
              "Overhead is every factory cost that is not direct materials or direct labor."]),
        part(qs[1], K(dm + dl + oh), [K(oh), K(dm + dl), K(allc)],
             [f"Product costs = DM {K(dm)} + DL {K(dl)} + Overhead {K(oh)} = {K(dm + dl + oh)}"]),
        part(qs[2], K(per), [K(dm + dl + oh), K(per - items[-1][1] if items[-1][2] == "PER" else per - 1), K(allc)],
             [f"Period costs = {names('PER')} = {K(per)}",
              "These are selling and administrative costs, not factory costs."])])

# 7: total manufacturing cost and COGS (three inventories)
def t7(intro, rm, wip, fg, purch, dl, oh, q1, q2, period):
    used = rm[0] + purch - rm[1]; tmc = used + dl + oh
    cogm = tmc + wip[0] - wip[1]; cogs = cogm + fg[0] - fg[1]
    t = tbl([["Raw materials inventory", K(rm[0]), K(rm[1])], ["Work in process inventory", K(wip[0]), K(wip[1])],
             ["Finished goods inventory", K(fg[0]), K(fg[1])]], ["", "Beginning", "Ending"])
    return dict(topic="Cost of goods manufactured and sold", stem=intro + t + period, parts=[
        part(q1, K(tmc), [K(purch + dl + oh), K(cogm), K(cogs)] if len({tmc, purch + dl + oh, cogm, cogs}) == 4 else [K(purch + dl + oh), K(cogm), K(tmc - 100)],
             [f"Raw materials used = {K(rm[0])} + {K(purch)} − {K(rm[1])} = {K(used)}",
              f"Total manufacturing costs = {K(used)} + {K(dl)} + {K(oh)} = {K(tmc)}"]),
        part(q2, K(cogs), [K(cogm), K(cogm - fg[0] + fg[1]), K(tmc)],
             [f"Cost of goods manufactured = {K(tmc)} + {K(wip[0])} − {K(wip[1])} = {K(cogm)}",
              f"Cost of goods sold = {K(cogm)} + {K(fg[0])} − {K(fg[1])} = {K(cogs)}"])])

# 8: DM used, COGM, COGS from a list
def t8(intro, dmb, wipb, fgb, dme, wipe, fge, purch, dl, oh, qs):
    used = dmb + purch - dme; tmc = used + dl + oh; cogm = tmc + wipb - wipe; cogs = cogm + fgb - fge
    rows = [["Beginning direct materials inventory", K(dmb)], ["Beginning work in process", K(wipb)],
            ["Beginning finished goods", K(fgb)], ["Ending direct materials inventory", K(dme)],
            ["Ending work in process", K(wipe)], ["Ending finished goods", K(fge)],
            ["Purchases of direct materials", K(purch)], ["Direct labor", K(dl)], ["Factory overhead", K(oh)]]
    return dict(topic="Cost of goods manufactured and sold", stem=intro + tbl(rows), parts=[
        part(qs[0], K(used), [K(purch), K(purch - dmb + dme), K(dmb + purch)],
             [f"Direct materials used = {K(dmb)} + {K(purch)} − {K(dme)} = {K(used)}"]),
        part(qs[1], K(cogm), [K(tmc), K(tmc - wipb + wipe), K(cogs)],
             [f"Total manufacturing costs = {K(used)} + {K(dl)} + {K(oh)} = {K(tmc)}",
              f"COGM = {K(tmc)} + {K(wipb)} − {K(wipe)} = {K(cogm)}"]),
        part(qs[2], K(cogs), [K(cogm), K(cogm - fgb + fge), K(tmc)],
             [f"COGS = COGM + Beginning FG − Ending FG = {K(cogm)} + {K(fgb)} − {K(fge)} = {K(cogs)}"])])

# 9: high-low cost equation
def eq(a, b, per): return f"Total cost = {P(a)} + {P(b, 2)} per {per}"
def t9(intro, data, per, head, q, wrong):
    hi = max(data); lo = min(data)
    b = (hi[1] - lo[1]) / (hi[0] - lo[0]); a = hi[1] - b * hi[0]
    t = tbl([[num(x), P(y)] for x, y in data], head)
    return dict(topic="High-low method", stem=intro + t + q, parts=[part("", eq(a, b, per),
        [eq(x, y, per) for x, y in wrong],
        [f"Use the highest and lowest ACTIVITY levels (not the highest and lowest costs): {num(hi[0])} and {num(lo[0])}",
         f"Variable rate = ({P(hi[1])} − {P(lo[1])}) ÷ ({num(hi[0])} − {num(lo[0])}) = {P(hi[1] - lo[1])} ÷ {num(hi[0] - lo[0])} = {P(b, 2)} per {per}",
         f"Fixed cost = {P(hi[1])} − {P(b, 2)} × {num(hi[0])} = {P(a)}",
         f"Cost formula: y = {P(a)} + {P(b, 2)}x"])])

# 10: high-low estimate
def t10(stem, hi, lo, x, per, wrong):
    b = (hi[1] - lo[1]) / (hi[0] - lo[0]); a = hi[1] - b * hi[0]; est = a + b * x
    return dict(topic="High-low method", stem=stem, parts=[part("", P(est), [P(w) for w in wrong],
        [f"Variable rate = ({P(hi[1])} − {P(lo[1])}) ÷ ({num(hi[0])} − {num(lo[0])}) = {P(b, 2)} per {per}",
         f"Fixed cost = {P(hi[1])} − {P(b, 2)} × {num(hi[0])} = {P(a)}",
         f"Estimated cost = {P(a)} + {P(b, 2)} × {num(x)} = {P(est)}"])])

def batch(v):
    out = []
    if v == 1:
        out.append(t1("A company's direct materials inventory was ₱40,000 on March 1 and ₱52,000 on March 31. Other manufacturing data for March:", 40, 52, 120, 75, 95,
                      "Q1: How much prime cost was added to production during March?", "Q2: How much conversion cost was added to production during March?"))
        out.append(t2a("A company's prime costs total ₱2,400,000. Manufacturing overhead is ₱900,000 and direct labor is ₱650,000. How much are direct materials?", 2400, 900, 650))
        out.append(t3("A company's records show: direct materials used, ₱210,000; direct labor, ₱380,000; manufacturing overhead, ₱290,000; and selling and administrative expenses, ₱260,000. How much are total product costs?", 210, 380, 290, [260]))
        out.append(t4("A company's records include these costs: sales salaries, ₱55,000; factory rent, ₱72,000; administrative expenses, ₱160,000; and advertising, ₱38,000. How much are total period costs?",
                      [("sales salaries", 55, True), ("factory rent", 72, False), ("administrative expenses", 160, True), ("advertising", 38, True)], [160, 215, 325]))
        out.append(t5("Total costs are ₱150,000 when 20,000 units are produced. Of this amount, ₱60,000 is variable. What will total costs be at 25,000 units?", 20, 150, 60, True, 25))
        out.append(t6("The following costs were incurred during the period:", [
            ("Direct materials", 140, "DM"), ("Factory utilities", 8, "OH"), ("Office rent", 36, "PER"), ("Indirect materials", 12, "OH"),
            ("Sales salaries", 52, "PER"), ("Depreciation of factory equipment", 24, "OH"), ("Depreciation of delivery trucks", 15, "PER"),
            ("Direct labor", 150, "DL"), ("Advertising", 90, "PER")],
            ["Q1: How much is total manufacturing overhead?", "Q2: How much are total product costs?", "Q3: How much are total period costs?"]))
        out.append(t7("Mabini Manufacturing's inventory records for June show:", (180, 220), (140, 110), (200, 260), 640, 520, 430,
                      "Q1: How much were total manufacturing costs for June?", "Q2: How much is the cost of goods sold for June?",
                      "<p>During June, raw materials purchased were ₱640,000, direct labor was ₱520,000, and manufacturing overhead was ₱430,000.</p>"))
        out.append(t8("A company reported the following for the period:", 35, 45, 60, 25, 70, 90, 210, 180, 240,
                      ["Q1: How much direct materials were used during the period?", "Q2: How much is the cost of goods manufactured?", "Q3: How much is the cost of goods sold?"]))
        out.append(t9("A company gathered these production and cost figures for the past four months:", [(2400, 31200), (2200, 31800), (1800, 25800), (1500, 23100)],
                      "unit", ["Units produced", "Total cost"], "<p>Using the high-low method, what is the monthly cost formula?</p>",
                      [(0, 13), (12000, 8), (7200, 10)]))
        out.append(t10("Last year, a company's busiest month had 50,000 machine hours and utility costs of ₱96,000. Its slowest month had 30,000 machine hours and utility costs of ₱66,000. Using the high-low method, estimate utility costs for a month with 42,000 machine hours.",
                       (50000, 96000), (30000, 66000), 42000, "machine hour", [80640, 63000, 92400]))
    if v == 2:
        out.append(t1("On April 1, a company had ₱25,000 of direct materials on hand; on April 30, it had ₱18,000. April manufacturing data:", 25, 18, 90, 64, 71,
                      "Q1: Compute the prime cost added to production in April.", "Q2: Compute the conversion cost added to production in April."))
        out.append(t2b("Conversion costs are ₱1,700,000, of which ₱1,180,000 is manufacturing overhead. Prime costs are ₱1,800,000. What is the cost of direct materials?", 1700, 1180, 1800))
        out.append(t3("For the year, a company incurred: direct materials used, ₱145,000; direct labor, ₱225,000; factory overhead, ₱310,000; selling expenses, ₱95,000; and administrative expenses, ₱130,000. What is the total of product costs?", 145, 225, 310, [95, 130]))
        out.append(t4("These costs were recorded during the month: delivery expense, ₱26,000; factory insurance, ₱18,000; depreciation of office building, ₱44,000; factory supervisor's salary, ₱85,000; and company president's salary, ₱120,000. Compute total period costs.",
                      [("delivery expense", 26, True), ("factory insurance", 18, False), ("office depreciation", 44, True), ("factory supervisor's salary", 85, False), ("president's salary", 120, True)], [293, 164, 103]))
        out.append(t5("At 8,000 units, a company's total costs are ₱96,000, including ₱56,000 of fixed costs. What will total costs be if production drops to 6,000 units?", 8, 96, 56, False, 6))
        out.append(t6("A company's costs for the period are listed below:", [
            ("Direct materials", 98, "DM"), ("Indirect labor", 30, "OH"), ("Salespersons' commissions", 41, "PER"), ("Factory property taxes", 9, "OH"),
            ("CEO's salary", 75, "PER"), ("Factory machine repairs", 13, "OH"), ("Office supplies", 6, "PER"), ("Direct labor", 112, "DL"), ("Marketing", 64, "PER")],
            ["Q1: What is the total manufacturing overhead?", "Q2: What is the total of product costs?", "Q3: What is the total of period costs?"]))
        out.append(t7("Luzon Fabricators shows these inventory balances for May:", (95, 70), (120, 150), (80, 65), 410, 330, 290,
                      "Q1: What were the total manufacturing costs incurred in May?", "Q2: What is May's cost of goods sold?",
                      "<p>In May, the company bought ₱410,000 of raw materials, incurred ₱330,000 of direct labor, and spent ₱290,000 on manufacturing overhead.</p>"))
        out.append(t8("Data for the year:", 50, 30, 75, 62, 48, 55, 260, 210, 190,
                      ["Q1: Compute direct materials used.", "Q2: Compute the cost of goods manufactured.", "Q3: Compute the cost of goods sold."]))
        out.append(t9("Maintenance costs and machine hours for the past four months were:", [(5000, 46000), (6200, 53000), (8000, 64000), (7100, 59600)],
                      "machine hour", ["Machine hours", "Maintenance cost"], "<p>Based on the high-low method, which cost formula should the company use?</p>",
                      [(0, 8), (22000, 5), (14000, 6.25)]))
        out.append(t10("A company produced 80,000 units in October, its highest month, and 35,000 units in February, its lowest. Power costs were ₱142,000 in October and ₱79,000 in February. Using the high-low method, estimate power costs for a month with 60,000 units.",
                       (80000, 142000), (35000, 79000), 60000, "unit", [106500, 84000, 120000]))
    if v == 3:
        out.append(t1("Direct materials on hand were ₱60,000 at the start of August and ₱45,000 at the end. Additional data for August:", 60, 45, 150, 110, 125,
                      "Q1: What prime cost was added to production in August?", "Q2: What conversion cost was added to production in August?"))
        out.append(t2a("Manufacturing overhead is ₱1,400,000, direct labor is ₱1,150,000, and prime costs amount to ₱3,200,000. Determine the cost of direct materials.", 3200, 1400, 1150))
        out.append(t3("Costs for the quarter: direct materials used ₱260,000; direct labor ₱410,000; manufacturing overhead ₱335,000; selling and administrative expenses ₱180,000. Total product costs are:", 260, 410, 335, [180]))
        out.append(t4("Selected costs for the year: advertising, ₱64,000; factory utilities, ₱21,000; office salaries, ₱118,000; plant manager's salary, ₱90,000; and sales commissions, ₱47,000. Period costs total:",
                      [("advertising", 64, True), ("factory utilities", 21, False), ("office salaries", 118, True), ("plant manager's salary", 90, False), ("sales commissions", 47, True)], [340, 182, 111]))
        out.append(t5("When 30,000 units are produced, total costs are ₱240,000, of which ₱90,000 are variable. Compute total costs at 36,000 units.", 30, 240, 90, True, 36))
        out.append(t6("Below are the costs incurred during the month:", [
            ("Direct materials", 175, "DM"), ("Factory supervisor's salary", 40, "OH"), ("Office utilities", 11, "PER"), ("Lubricants for factory machines", 7, "OH"),
            ("Sales commissions", 58, "PER"), ("Factory insurance", 16, "OH"), ("Accounting staff salaries", 66, "PER"), ("Direct labor", 190, "DL"), ("Promotional materials", 29, "PER")],
            ["Q1: Manufacturing overhead totals:", "Q2: Product costs total:", "Q3: Period costs total:"]))
        out.append(t7("Visayas Woodcraft's inventories for September were:", (150, 120), (90, 125), (175, 160), 520, 460, 380,
                      "Q1: Total manufacturing costs for September amounted to:", "Q2: Cost of goods sold for September is:",
                      "<p>September purchases of raw materials were ₱520,000. Direct labor was ₱460,000 and manufacturing overhead was ₱380,000.</p>"))
        out.append(t8("The following data relate to a manufacturer's operations for the year:", 42, 66, 88, 30, 54, 101, 230, 205, 260,
                      ["Q1: Direct materials used were:", "Q2: Cost of goods manufactured was:", "Q3: Cost of goods sold was:"]))
        out.append(t9("Supplies cost and direct labor hours for four months were:", [(3000, 18600), (4200, 25500), (2000, 14400), (4500, 24900)],
                      "direct labor hour", ["Direct labor hours", "Supplies cost"], "<p>Using the high-low method, the cost formula for supplies is:</p>",
                      [(8400, 3.6), (0, 5.5), (5400, 4.4)]))
        out.append(t10("At 12,000 direct labor hours, indirect labor cost was ₱55,200; at 7,000 hours, it was ₱37,700. These were the year's high and low activity levels. Using the high-low method, what is the expected indirect labor cost at 9,500 hours?",
                       (12000, 55200), (7000, 37700), 9500, "direct labor hour", [43700, 33250, 48000]))
    if v == 4:
        out.append(t1("A company started November with ₱18,000 of direct materials and ended with ₱27,000. November data:", 18, 27, 132, 88, 104,
                      "Q1: Prime cost added to production in November was:", "Q2: Conversion cost added to production in November was:"))
        out.append(t2b("A company's conversion costs are ₱2,250,000 and its prime costs are ₱2,700,000. Manufacturing overhead is ₱1,320,000. How much is direct materials?", 2250, 1320, 2700))
        out.append(t3("A manufacturer recorded: direct materials used, ₱320,000; direct labor, ₱275,000; factory overhead, ₱405,000; selling expenses, ₱150,000; and general and administrative expenses, ₱85,000. How much should be treated as product costs?", 320, 275, 405, [150, 85]))
        out.append(t4("Costs incurred for the period: store rent, ₱48,000; depreciation of factory building, ₱60,000; freight-out, ₱17,000; factory janitor's wages, ₱22,000; office staff salaries, ₱95,000; and bad debts expense, ₱9,000. How much are period costs?",
                      [("store rent", 48, True), ("factory building depreciation", 60, False), ("freight-out", 17, True), ("factory janitor's wages", 22, False), ("office staff salaries", 95, True), ("bad debts", 9, True)], [251, 160, 82]))
        out.append(t5("Total costs at 15,000 units are ₱210,000. Fixed costs make up ₱120,000 of this. How much will total costs be at 18,000 units?", 15, 210, 120, False, 18))
        out.append(t6("A manufacturer incurred these costs during the month:", [
            ("Direct materials", 205, "DM"), ("Plant security", 18, "OH"), ("Sales manager's salary", 54, "PER"), ("Small tools used in the factory", 6, "OH"),
            ("Depreciation of showroom", 21, "PER"), ("Factory heat and light", 15, "OH"), ("Legal fees, head office", 12, "PER"), ("Direct labor", 230, "DL"), ("Sales travel", 33, "PER")],
            ["Q1: Compute total manufacturing overhead.", "Q2: Compute total product costs.", "Q3: Compute total period costs."]))
        out.append(t7("Mindanao Metalworks reported these inventories for December:", (110, 135), (200, 170), (95, 120), 480, 390, 350,
                      "Q1: How much are December's total manufacturing costs?", "Q2: How much is December's cost of goods sold?",
                      "<p>December raw material purchases totaled ₱480,000, direct labor was ₱390,000, and manufacturing overhead was ₱350,000.</p>"))
        out.append(t8("Information from a company's records:", 28, 52, 64, 36, 40, 58, 186, 154, 172,
                      ["Q1: How much direct materials were used?", "Q2: What is the cost of goods manufactured?", "Q3: What is the cost of goods sold?"]))
        out.append(t9("A courier company recorded the following deliveries and costs:", [(900, 21500), (1400, 29000), (1250, 29800), (700, 18500)],
                      "delivery", ["Deliveries", "Total delivery cost"], "<p>Using the high-low method, what is the cost formula?</p>",
                      [(8000, 16), (5000, 17), (10500, 13.5)]))
        out.append(t10("Machine hours peaked at 28,000 in August, when repair costs were ₱74,600, and were lowest at 16,000 in January, when repair costs were ₱52,400. Using the high-low method, what repair cost should be expected at 22,000 machine hours?",
                       (28000, 74600), (16000, 52400), 22000, "machine hour", [40700, 68000, 58000]))
    return out

for v in (1, 2, 3, 4):
    Q.extend(batch(v))
random.seed(510)
for qq in Q:
    for p in qq["parts"]:
        o = p["opts"][:]; random.shuffle(o); p["opts"] = o; p["ans"] = o.index(p["correct"])

if __name__ == "__main__":
    for i, qq in enumerate(Q, 1):
        for p in qq["parts"]:
            print(i, qq["topic"][:26], "|", p["correct"], "|", p["opts"], "|", p["sol"][-1][:90])

from fractions import Fraction as Fr
import random

def num(x, dec=None):
    x = float(x)
    if dec is None:
        dec = 0 if abs(x - round(x)) < 1e-9 else 2
    return f"{x:,.{dec}f}"
def P(x, dec=None): return "₱" + num(x, dec)
def P2(x): return "₱" + num(x, 2)
def pct(x):
    v = float(x) * 100
    return (f"{v:.0f}%" if abs(v - round(v)) < 1e-9 else (f"{v:.1f}%" if abs(v*10 - round(v*10)) < 1e-9 else f"{v:.2f}%"))
def U(x): return num(x, 0) + " units" if False else num(x, 0)

def tbl(rows, head=None):
    h = ""
    if head:
        h = "<thead><tr>" + "".join(f"<th>{c}</th>" for c in head) + "</tr></thead>"
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tw"><table>{h}<tbody>{b}</tbody></table></div>'

def part(q, correct, wrongs, sol):
    opts = [correct] + [w for w in wrongs]
    assert len(set(opts)) == 4, (q, opts)
    return dict(q=q, correct=correct, opts=opts, sol=sol)

Q = []  # list of dict(stem, parts, topic)

# ---------- 1: BEP units from CM ratio ----------
def q1(stem, p, r, F):
    cm = p * r; be = F / cm
    sol = [f"CM per unit = {P2(p)} × {pct(r)} = {P2(cm)}",
           f"BEP units = Fixed costs ÷ CM per unit = {P(F)} ÷ {P2(cm)} = {num(be)} units"]
    return dict(topic="Break-even point in units", stem=stem, parts=[part("", num(be),
        [num(F / p), num(F / (p * (1 - r))), num(F / r)], sol)])
# ---------- 2/6: margin of safety ----------
def q2(stem, F, r, S, monthly=False):
    be = F / r; mos = S - be
    sol = [f"BEP sales = Fixed costs ÷ CM ratio = {P(F)} ÷ {pct(r)} = {P(be)}",
           f"Margin of safety = Sales − BEP sales = {P(S)} − {P(be)} = {P(mos)}"]
    w = [P(S * r), P(F), P(be)] if not monthly else [P(S - F / (1 - r)), P(F / (1 - r)), P(be)]
    return dict(topic="Margin of safety", stem=stem, parts=[part("", P(mos), w, sol)])
# ---------- 3: MOS ratio ----------
def q3(stem, Uu, B, price):
    m = Fr(Uu - B, Uu)
    sol = [f"Margin of safety = {num(Uu)} − {num(B)} = {num(Uu - B)} units",
           f"MOS ratio = Margin of safety ÷ Sales = {num(Uu - B)} ÷ {num(Uu)} = {pct(m)}",
           f"(Same in pesos: {P((Uu - B) * price)} ÷ {P(Uu * price)} = {pct(m)})"]
    return dict(topic="Margin of safety ratio", stem=stem, parts=[part("", pct(m),
        [pct(Fr(Uu - B, B)), pct(Fr(B, Uu)), pct(Fr(Uu, B))], sol)])
# ---------- 4: max variable cost ----------
def q4(stem, F, N, I, t, p):
    pre = I / (1 - t); cm = (F + pre) / N; vc = p - cm
    sol = [f"Profit before tax = Profit after tax ÷ (100% − tax rate) = {P(I)} ÷ {pct(1 - t)} = {P(pre)}",
           f"Required CM per unit = (Fixed costs + Profit) ÷ Units = ({P(F)} + {P(pre)}) ÷ {num(N)} = {P2(cm)}",
           f"Maximum VC per unit = Price − CM per unit = {P2(p)} − {P2(cm)} = {P2(vc)}"]
    return dict(topic="Target profit after tax", stem=stem, parts=[part("", P2(vc),
        [P2(p - (F + I) / N), P2(cm), P2(p - F / N)], sol)])
# ---------- 5: price at BEP ----------
def q5(stem, N, V, F):
    pr = (V + F) / N
    sol = ["At break-even, Sales = Variable costs + Fixed costs",
           f"Sales = {P(V)} + {P(F)} = {P(V + F)}",
           f"Price per unit = {P(V + F)} ÷ {num(N)} units = {P2(pr)}"]
    return dict(topic="Break-even equation", stem=stem, parts=[part("", P2(pr),
        [P2((V - F) / N), P2(F / N), "Not enough information"], sol)])
# ---------- 7: overall CM ratio ----------
def q7(stem_fn, names, price, prod, sa, units, F):
    cm = [price[i] - prod[i] - sa[i] for i in range(2)]
    sales = [price[i] * units[i] for i in range(2)]
    tcm = [cm[i] * units[i] for i in range(2)]
    r = Fr(sum(tcm), sum(sales))
    sol = [f"CM per unit: {names[0]} = {P(price[0])} − {P(prod[0])} − {P(sa[0])} = {P(cm[0])}; {names[1]} = {P(price[1])} − {P(prod[1])} − {P(sa[1])} = {P(cm[1])}",
           f"Total CM = {num(units[0])}({P(cm[0])}) + {num(units[1])}({P(cm[1])}) = {P(tcm[0])} + {P(tcm[1])} = {P(sum(tcm))}",
           f"Total sales = {num(units[0])}({P(price[0])}) + {num(units[1])}({P(price[1])}) = {P(sum(sales))}",
           f"Weighted-average CM ratio = {P(sum(tcm))} ÷ {P(sum(sales))} = {pct(r)}",
           "Fixed costs are not needed for this question."]
    avg = (Fr(cm[0], price[0]) + Fr(cm[1], price[1])) / 2
    noSA = Fr(sum((price[i] - prod[i]) * units[i] for i in range(2)), sum(sales))
    wr = [pct(avg), pct(Fr(cm[0], price[0])), pct(Fr(cm[1], price[1])), pct(noSA)]
    wr = [w for w in dict.fromkeys(wr) if w != pct(r)][:3]
    table = tbl([["Selling price per unit", P(price[0]), P(price[1])],
                 ["Variable production cost per unit", P(prod[0]), P(prod[1])],
                 ["Variable selling &amp; admin. expense per unit", P(sa[0]), P(sa[1])],
                 ["Expected unit sales", num(units[0]), num(units[1])]], ["", names[0], names[1]])
    return dict(topic="Sales mix: weighted CM ratio", stem=stem_fn(table), parts=[part("", pct(r), wr, sol)])
# ---------- 8: three-product BEP ----------
def q8(stem, names, mix, cms, F, ask, wrong):
    pk = sum(m * c for m, c in zip(mix, cms)); packs = F / pk; ans = packs * mix[ask]
    sol = [f"Sales mix {names[0]} : {names[1]} : {names[2]} = {mix[0]} : {mix[1]} : {mix[2]}",
           f"CM per package = {mix[0]}({P2(cms[0])}) + {mix[1]}({P2(cms[1])}) + {mix[2]}({P2(cms[2])}) = {P2(pk)}",
           f"Break-even packages = {P(F)} ÷ {P2(pk)} = {num(packs)}",
           f"Units of {names[ask]} = {num(packs)} × {mix[ask]} = {num(ans)}"]
    return dict(topic="Sales mix: three products", stem=stem, parts=[part("", num(ans), [num(w) for w in wrong], sol)])
# ---------- 9: CM ratio from BEP ----------
def q9(stem, p, B, F, wrong):
    cmu = F / B; r = Fr(cmu).limit_denominator(1000) / Fr(p)
    sol = [f"CM per unit = Fixed costs ÷ BEP units = {P(F)} ÷ {num(B)} = {P2(cmu)}",
           f"CM ratio = CM per unit ÷ Price = {P2(cmu)} ÷ {P2(p)} = {pct(r)}"]
    return dict(topic="Working back to CM ratio", stem=stem, parts=[part("", pct(r), wrong, sol)])
# ---------- 10: profit from BEP sales ----------
def q10(stem, F, Sb, S):
    r = Fr(F, Sb); pr = (S - Sb) * r
    sol = [f"CM ratio = Fixed costs ÷ BEP sales = {P(F)} ÷ {P(Sb)} = {pct(r)}",
           f"Profit = (Sales − BEP sales) × CM ratio = ({P(S)} − {P(Sb)}) × {pct(r)} = {P(pr)}",
           "Only sales above break-even produce profit."]
    return dict(topic="Profit from margin of safety", stem=stem, parts=[part("", P(pr), [P(S * r), P(S - Sb), P(F)], sol)])
# ---------- 11: work back price; MOS ----------
def q11(intro, vsa, vpr, fsa, fpr, q1t, N, prof, q2t, N2, p2):
    vc = vsa + vpr; F = fsa + fpr
    pr = Fr(F + prof, N) + vc
    t = tbl([["Variable costs per unit", "", ""], ["&nbsp;&nbsp;Selling, general &amp; admin.", P2(vsa), ""],
             ["&nbsp;&nbsp;Production", P2(vpr), ""], ["Fixed costs per year", "", ""],
             ["&nbsp;&nbsp;Selling, general &amp; admin.", P(fsa), ""], ["&nbsp;&nbsp;Production", P(fpr), ""]])
    t = tbl([["<b>Variable costs</b>", ""], ["SG&amp;A", P2(vsa) + " per unit"], ["Production", P2(vpr) + " per unit"],
             ["<b>Fixed costs</b>", ""], ["SG&amp;A", P(fsa) + " per year"], ["Production", P(fpr) + " per year"]])
    s1 = [f"Total VC per unit = {P2(vsa)} + {P2(vpr)} = {P2(vc)}; Total fixed costs = {P(fsa)} + {P(fpr)} = {P(F)}",
          f"Sales = VC + FC + Profit → {num(N)}p = {num(N)}({P2(vc)}) + {P(F)} + {P(prof)}",
          f"Price = {P2(vc)} + ({P(F)} + {P(prof)}) ÷ {num(N)} = {P2(vc)} + {P2(Fr(F + prof, N))} = {P2(pr)}"]
    cm2 = p2 - vc; be = Fr(F, cm2); mos = (N2 - be) * p2
    s2 = [f"CM per unit = {P2(p2)} − {P2(vc)} = {P2(cm2)}",
          f"BEP units = {P(F)} ÷ {P2(cm2)} = {num(be)} units",
          f"Margin of safety = ({num(N2)} − {num(be)}) × {P2(p2)} = {P(mos)}"]
    return dict(topic="Working back: price and margin of safety", stem=intro + t, parts=[
        part(q1t, P2(pr), [P2(Fr(F + prof, N)), P2(vc + Fr(F, N)), P2(vc + Fr(prof, N))], s1),
        part(q2t, P(mos), [P((N2 - be) * cm2), P(be * p2), P(N2 * p2)], s2)])
# ---------- 12: DOL ----------
def q12(intro, dol, pm, mos, r, q1t, x, q2t, d):
    t = tbl([["Degree of operating leverage", num(dol, 1)], ["Profit margin percentage", pct(pm)],
             ["Margin of safety percentage", pct(mos)], ["Contribution margin ratio", pct(r)]])
    s1 = [f"% change in profit = % change in sales × DOL = {pct(x)} × {num(dol, 1)} = {pct(x * dol)}"]
    s2 = ["To keep profit the same, the extra CM must cover the added fixed cost.",
          f"Required sales increase = Added fixed cost ÷ CM ratio = {P(d)} ÷ {pct(r)} = {P(d / r)}"]
    return dict(topic="Degree of operating leverage", stem=intro + t, parts=[
        part(q1t, pct(x * dol), [pct(x * pm), pct(x * mos), pct(x * r)], s1),
        part(q2t, P(d / r), [P(d), P(d / mos), P(d / pm)], s2)])
# ---------- 13: income statement ----------
def q13(intro, S, V, F, k, qts):
    cm = S - V; r = Fr(cm, S); pr = cm - F; be = F / r; mos = S - be
    newp = cm * k - F; dol = Fr(cm, pr)
    t = tbl([["Sales", P(S)], ["Variable costs", f"({num(V)})"], ["Contribution margin", P(cm)],
             ["Fixed costs", f"({num(F)})"], ["Profit before taxes", P(pr)]])
    parts = [
        part(qts[0], P(be), [P(F), P(cm), P(V + F)],
             [f"CM ratio = {P(cm)} ÷ {P(S)} = {pct(r)}", f"BEP sales = {P(F)} ÷ {pct(r)} = {P(be)}"]),
        part(qts[1], P(mos), [P(pr), P(F), P(S - F)],
             [f"Margin of safety = Sales − BEP sales = {P(S)} − {P(be)} = {P(mos)}"]),
        part(qts[2], P(newp), [P(pr * k), P(cm * k), P(S * (k - 1))],
             [f"New CM = {P(cm)} × {pct(k)} = {P(cm * k)}",
              f"Profit = New CM − Fixed costs = {P(cm * k)} − {P(F)} = {P(newp)}",
              "Fixed costs stay the same; only CM grows with sales."]),
        part(qts[3], num(dol, 2), [num(Fr(S, cm), 2), num(Fr(S, pr), 2), num(Fr(cm, F), 2)],
             [f"DOL = Contribution margin ÷ Profit before tax = {P(cm)} ÷ {P(pr)} = {num(dol, 2)}"]),
    ]
    return dict(topic="CVP from an income statement", stem=intro + t, parts=parts)

def q40():
    rows = [["Materials cost per unit", "₱14.00", "₱14.50"], ["Labor cost per unit", "9.00", "3.00"],
            ["Other variable cost per unit", "2.00", "3.50"], ["Rent per year", "40,000", "96,000"],
            ["Maintenance per year", "8,000", "16,000"]]
    stem = ("A bakery is choosing between keeping its manual line and switching to a robotic line. Data for each option:" +
            tbl(rows, ["", "Manual line", "Robotic line"]) +
            "At what annual volume will the two options cost the same?")
    sol = ["Manual: VC = 14 + 9 + 2 = ₱25.00 per unit; FC = 40,000 + 8,000 = ₱48,000",
           "Robotic: VC = 14.50 + 3 + 3.50 = ₱21.00 per unit; FC = 96,000 + 16,000 = ₱112,000",
           "Indifference point: 48,000 + 25x = 112,000 + 21x → 4x = 64,000 → x = 16,000 units",
           "Below 16,000 units the manual line is cheaper; above it the robotic line is cheaper."]
    return dict(topic="Indifference point (bonus)", stem=stem, parts=[part("", "16,000 units",
        ["12,000 units", "28,000 units", "14,000 units"], sol)])

def batch(b):
    out = []
    if b == 1:
        out.append(q1("A company that sells only one product expects the following for next year: selling price of ₱2.40 per unit, contribution margin ratio of 40%, and total fixed expenses of ₱345,600. How many units must it sell to break even?", Fr("2.4"), Fr(40, 100), 345600))
        out.append(q2("A company has fixed costs of ₱180,000 and a contribution margin ratio of 45%. Current sales are ₱600,000. What is the margin of safety?", 180000, Fr(45, 100), 600000))
        out.append(q3("A firm sold 80,000 units at ₱25 each last year, for total sales of ₱2,000,000. Its break-even point was 60,000 units. What is the margin of safety ratio?", 80000, 60000, 25))
        out.append(q4("A company incurs annual fixed costs of ₱300,000 and expects to sell 150,000 units at ₱7 each. Management wants an after-tax income of ₱90,000, and the tax rate is 25%. What is the most the company can spend on variable costs per unit and still meet its profit goal?", 300000, 150000, 90000, Fr(25, 100), 7))
        out.append(q5("At the break-even point of 4,000 units, variable costs are ₱96,000 and fixed costs are ₱60,000. How much is the selling price per unit?", 4000, 96000, 60000))
        out.append(q2("A company sells a single product for ₱20 per unit. Fixed costs are ₱99,000 per month, and the contribution margin ratio is 45%. If actual sales for the month are ₱300,000, what is the margin of safety?", 99000, Fr(45, 100), 300000, True))
        out.append(q7(lambda t: "A company produces two products, A and B. Data per unit:" + t + "Fixed expenses are budgeted at ₱300,000 per year. What is the company's overall contribution margin ratio for the expected sales mix?", ["A", "B"], [80, 150], [40, 60], [8, 15], [5000, 4000], 300000))
        out.append(q8("A manufacturer sells products A, B and C. It sells two units of A for each unit of C, and three units of B for each unit of A. Contribution margins are ₱2 per unit of A, ₱1 per unit of B and ₱4 per unit of C. Fixed costs are ₱1,400,000. How many units of A would the manufacturer sell at the break-even point?", ["A", "B", "C"], [2, 6, 1], [2, 1, 4], 1400000, 0, [100000, 600000, 700000]))
        out.append(q9("A company sells only one product, priced at ₱12 per unit. Its projected break-even point is 40,000 units, and fixed costs are projected at ₱144,000. What is the projected contribution margin ratio?", 12, 40000, 144000, ["20%", "60%", "70%"]))
        out.append(q10("A manufacturer has fixed costs of ₱300,000 and break-even sales of ₱1,200,000. What is the projected profit at ₱1,800,000 of sales?", 300000, 1200000, 1800000))
        out.append(q11("A company produces and sells a single product. Its costs are as follows:", 3, 5, 18000, 22000,
                       "Q1: It produced and sold 8,000 units and earned a profit of ₱24,000. What was the selling price per unit?", 8000, 24000,
                       "Q2: Next year it expects to produce and sell 6,000 units at ₱18 per unit. Unit variable costs and total fixed costs stay the same. What is the projected margin of safety?", 6000, 18))
        out.append(q12("The following information relates to Mayon Company:", 4, Fr(10, 100), Fr(25, 100), Fr(40, 100),
                       "Q1: If sales increase by 15%, by what percentage will net operating income increase?", Fr(15, 100),
                       "Q2: The company wants to give its sales staff a ₱48,000 salary increase but still keep the same net operating income. By how much would sales have to increase?", 48000))
        out.append(q13("Below is the income statement of a manufacturing company:", 500000, 200000, 240000, Fr(120, 100),
                       ["Q1: What is the break-even point in pesos?", "Q2: What is the margin of safety?",
                        "Q3: Fixed costs, unit price and unit variable cost stay the same. How much profit before taxes will the company make if sales rise to 120% of this year's level?",
                        "Q4: What is the degree of operating leverage?"]))
    if b == 2:
        out.append(q1("Next year, a one-product company will sell its product at ₱5.00 per unit. Its contribution margin ratio is 25%, and annual fixed costs total ₱150,000. What is its break-even point in units?", Fr(5), Fr(25, 100), 150000))
        out.append(q2("A company reports sales of ₱420,000. Its variable costs are 68% of sales, and fixed costs are ₱96,000. Compute the margin of safety in pesos.", 96000, Fr(32, 100), 420000))
        out.append(q3("A company sold 120,000 units at ₱30 each this year. Its break-even volume is 84,000 units. Compute the margin of safety percentage.", 120000, 84000, 30))
        out.append(q4("A company expects to sell 200,000 units next year at ₱9 per unit. Fixed costs are ₱480,000. It wants a net income after tax of ₱168,000, with a 30% income tax rate. What is the maximum variable cost per unit it can afford?", 480000, 200000, 168000, Fr(30, 100), 9))
        out.append(q5("A company breaks even when it sells 2,500 units. At that volume, total variable costs are ₱70,000 and fixed costs are ₱45,000. Compute the selling price per unit.", 2500, 70000, 45000))
        out.append(q2("A product sells for ₱12 per unit. Fixed costs are ₱57,600 per month, and variable costs are 60% of the selling price. Actual sales for the month are ₱200,000. How much is the margin of safety?", 57600, Fr(40, 100), 200000, True))
        out.append(q7(lambda t: "A company makes two products, X and Y. Per-unit data are as follows:" + t + "Annual fixed costs are ₱350,000. Compute the company's weighted-average contribution margin ratio.", ["X", "Y"], [50, 120], [25, 42], [5, 6], [12000, 3000], 350000))
        out.append(q8("For every unit of Z it sells, a company sells four units of X and two units of Y. Unit contribution margins are ₱3 for X, ₱5 for Y and ₱2 for Z. Fixed costs total ₱1,440,000. How many units of X must be sold to break even?", ["X", "Y", "Z"], [4, 2, 1], [3, 5, 2], 1440000, 0, [60000, 120000, 480000]))
        out.append(q9("Fixed costs are projected at ₱240,000, and the break-even point is 75,000 units. The company's sole product sells for ₱8 per unit. Compute the contribution margin ratio.", 8, 75000, 240000, ["30%", "60%", "75%"]))
        out.append(q10("A company's break-even sales are ₱800,000 and its fixed costs are ₱240,000. How much profit will it earn at sales of ₱1,400,000?", 240000, 800000, 1400000))
        out.append(q11("A single-product company has the following cost structure:", Fr("1.5"), Fr("4.5"), 9000, 21000,
                       "Q1: This year it made and sold 6,000 units, earning a profit of ₱12,000. What price did it charge per unit?", 6000, 12000,
                       "Q2: Next year it plans to sell 5,000 units at ₱14 per unit, with the same unit variable costs and total fixed costs. Compute the projected margin of safety.", 5000, 14))
        out.append(q12("Taal Corporation reports the following:", 2, Fr(15, 100), Fr(50, 100), Fr(30, 100),
                       "Q1: By what percentage will net operating income go up if sales increase by 10%?", Fr(10, 100),
                       "Q2: Management plans a ₱45,000 raise for the sales team and wants operating income to stay the same. How much additional sales are needed?", 45000))
        out.append(q13("A company's income statement shows the following:", 800000, 360000, 330000, Fr(125, 100),
                       ["Q1: Compute the break-even sales in pesos.", "Q2: How much is the margin of safety?",
                        "Q3: If next year's sales reach 125% of this year's, with the same price, unit variable cost and fixed costs, what will profit before taxes be?",
                        "Q4: Compute the degree of operating leverage."]))
    if b == 3:
        out.append(q1("A firm plans to price its only product at ₱2.00 per unit. Fixed costs for the year are ₱252,000, and variable costs are 70% of the selling price. How many units are needed to break even?", Fr(2), Fr(30, 100), 252000))
        out.append(q2("With a 35% contribution margin ratio and fixed costs of ₱140,000, a company currently sells ₱500,000. By how much can sales fall before the company starts to lose money?", 140000, Fr(35, 100), 500000))
        out.append(q3("Sales last year were ₱2,000,000 (50,000 units at ₱40 each). Break-even sales were 42,500 units. What percentage of sales is the margin of safety?", 50000, 42500, 40))
        out.append(q4("Selling price is ₱12 per unit, expected sales are 100,000 units, fixed costs are ₱360,000, and the desired profit after tax is ₱112,000 at a 20% tax rate. What is the highest variable cost per unit that still meets the profit goal?", 360000, 100000, 112000, Fr(20, 100), 12))
        out.append(q5("Fixed costs are ₱85,000. At the break-even volume of 5,000 units, variable costs total ₱135,000. How much does the company charge per unit?", 5000, 135000, 85000))
        out.append(q2("Monthly fixed costs are ₱72,000 for a product priced at ₱25 with a 40% contribution margin ratio. Sales this month reached ₱260,000. What is the margin of safety?", 72000, Fr(40, 100), 260000, True))
        out.append(q7(lambda t: "A firm sells products M and N. Information per unit:" + t + "Fixed costs are ₱400,000 per year. What overall contribution margin ratio does the expected sales mix produce?", ["M", "N"], [90, 200], [45, 70], [9, 10], [8000, 2400], 400000))
        out.append(q8("A company sells two units of Q and three units of R for every unit of P. Unit contribution margins are ₱6.00 for P, ₱2.50 for Q and ₱1.00 for R. Fixed costs are ₱2,100,000. At break-even, how many units of R will be sold?", ["P", "Q", "R"], [1, 2, 3], [6, Fr("2.5"), 1], 2100000, 2, [150000, 300000, 840000]))
        out.append(q9("A sole product priced at ₱15 breaks even at 36,000 units. Fixed costs are ₱270,000. What portion of each peso of sales is contribution margin?", 15, 36000, 270000, ["25%", "40%", "75%"]))
        out.append(q10("A company breaks even at ₱2,000,000 of sales. Its fixed costs are ₱360,000. Compute the operating profit at ₱2,500,000 of sales.", 360000, 2000000, 2500000))
        out.append(q11("Information on a company's single product:", Fr("2.5"), Fr("6.5"), 15000, 25000,
                       "Q1: At 10,000 units sold, the company earned ₱30,000. What was its unit selling price?", 10000, 30000,
                       "Q2: For next year it budgets 8,000 units at ₱17 each. Unit variable costs and total fixed costs do not change. What is the budgeted margin of safety?", 8000, 17))
        out.append(q12("Data for Banahaw Inc.:", 5, Fr(9, 100), Fr(20, 100), Fr(45, 100),
                       "Q1: Sales are expected to grow by 12%. What is the expected percentage increase in net operating income?", Fr(12, 100),
                       "Q2: The company will add ₱36,000 to sales salaries but wants to earn the same operating income. What increase in sales is required?", 36000))
        out.append(q13("Consider this income statement:", 600000, 210000, 299000, Fr(140, 100),
                       ["Q1: What sales in pesos are needed to break even?", "Q2: What is the margin of safety?",
                        "Q3: Assuming fixed costs and unit price and cost stay the same, what profit before taxes results if sales grow to 140% of the current level?",
                        "Q4: What is the degree of operating leverage?"]))
    return out

for b in (1, 2, 3):
    Q.extend(batch(b))
Q.append(q40())

random.seed(2026)
for qq in Q:
    for p in qq["parts"]:
        o = p["opts"][:]; random.shuffle(o)
        p["opts"] = o; p["ans"] = o.index(p["correct"])

if __name__ == "__main__":
    for i, qq in enumerate(Q, 1):
        for p in qq["parts"]:
            print(i, qq["topic"][:28], "|", p["correct"], "|", p["opts"], "|", p["sol"][-1][:80])

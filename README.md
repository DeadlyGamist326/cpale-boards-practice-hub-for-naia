# Accountancy Boards Practice Hub by Lax

A single-page practice hub for the Philippine CPA Licensure Exam (CPALE). Open `index.html` in any browser. It needs no server or install.

## Sections

**Management Services → Cost Concepts & Cost Behavior**
- **Handout**: manufacturing costs, prime and conversion cost, product vs. period costs, COGM and COGS, cost terms, cost behavior, high-low, scattergraph, least squares, correlation.
- **Questions (20)**: two sets of 10 problem types with different givens.

**Management Services → CVP Analysis**
- **Handout**: study notes on cost-volume-profit analysis. Covers contribution margin, break-even, target profit, margin of safety, sales mix, DOL, sensitivity and indifference point.
- **Questions (40)**: three sets of 13 board-style problem types with different givens, plus one bonus question. Each has a/b/c/d choices and a Reveal answer button that shows the step-by-step solution.
- **Sales Mix (5)**: two-product problems on break-even and profit targets.

## Editing

The page is generated, so edit the source files in `tools/` and rebuild:

```
python3 tools/build.py
```

| File | Contents |
|---|---|
| `tools/cost_questions.py`, `tools/cost_handout.html` | Cost Concepts topic |
| `tools/cvp_questions.py` | Question givens, wording, and answer and solution logic. Answers are computed, not typed. |
| `tools/cvp_handout.html` | Handout notes |
| `tools/sales_mix.html` | The 5 sales mix problems |
| `tools/build.py` | Assembles everything into `index.html`; the `TOPICS` list sets the home page boxes |

"""How each flashcard's question is shown (user request: every front must be an answerable question).

The card front in rfbt_flashcards.py stays the card's ID (crop keys and OVERRIDES use it); ASK maps it to
the question the reader sees. A "\n" starts a second line. In STEM cards the answer's lead-in line
(e.g. "The minimum requirements prescribed by laws and rules on:") moves to the question, so the answer
shows only the list."""

STEM = {  # front -> lead-in moved from the answer to the question (first OVERRIDES line is dropped)
 "Labor standards": "The minimum requirements prescribed by laws and rules on…",
 "Employer under RA 11199": "Any person, natural or juridical, domestic or foreign, who…",
 "Compensation under RA 11199": "All actual remuneration for employment, including…",
 "Declaration of basic policy of the Labor Code": "The State shall…",
}

ASK = {
 # ---- Social Security Law ----
 "The value a social security program must emphasize under RA 11199": "Under RA 11199, what value must a social security program emphasize?",
 "The hazards social security protects members against": "Against what hazards does social security protect members?",
 "Composition of the Social Security Commission (9 members)": "Who are the 9 members of the Social Security Commission?",
 "Term of office of the appointive Commission members": "What is the term of office of the appointive Commission members?",
 "Employer under RA 11199": "Who is an employer under RA 11199?",
 "Compensation under RA 11199": "What is compensation under RA 11199?",
 "Monthly salary credit": "What is the monthly salary credit, and what is the maximum MSC used for computing benefits?",
 "Services EXCLUDED from \"employment\" under RA 11199": "What services are EXCLUDED from \"employment\" under RA 11199?",
 "Primary beneficiaries": "Who are the primary beneficiaries?",
 "Share of dependent illegitimate children when there are legitimate children": "What is the share of dependent illegitimate children when there are legitimate children?",
 "Secondary beneficiaries": "Who are the secondary beneficiaries?",
 "Contingencies under RA 11199": "What are the contingencies under RA 11199?",
 "Average monthly salary credit (AMSC)": "How is the average monthly salary credit (AMSC) computed?",
 "Average daily salary credit (ADSC)": "How is the average daily salary credit (ADSC) computed?",
 "Semester": "What is a semester under RA 11199?",
 "Quarter": "What is a quarter under RA 11199?",
 "Credited years of service for a member covered in or after January 1985": "How are credited years of service counted for a member covered in or after January 1985?",
 "Self-employed persons who are compulsorily covered (examples)": "Which self-employed persons are compulsorily covered? Give examples.",
 "Deadline to remit SSS contributions": "When is the deadline to remit SSS contributions?",
 "Penalty for late remittance of contributions": "What is the penalty for late remittance of contributions?",
 "Prescriptive period for action against an employer for unpaid contributions": "What is the prescriptive period for an action against an employer for unpaid contributions?",
 "Minimum monthly pension": "How much is the minimum monthly pension, and with how many credited years of service?",
 "Additional benefit allowance for pensioners (from January 2017)": "How much is the additional benefit allowance for pensioners (from January 2017), and who gets it?",
 "Dependents' pension": "How much is the dependents' pension, and for which children?",
 "Death benefit when the member paid at least 36 monthly contributions before the semester of death": "What is the death benefit when the member paid at least 36 monthly contributions before the semester of death?",
 "Death benefit when the member paid FEWER than 36 monthly contributions": "What is the death benefit when the member paid FEWER than 36 monthly contributions?",
 "Permanent total disability benefit with at least 36 monthly contributions before the semester of disability": "What is the permanent total disability benefit with at least 36 monthly contributions before the semester of disability?",
 "Permanent total disability benefit with FEWER than 36 contributions": "What is the permanent total disability benefit with FEWER than 36 contributions?",
 "Disabilities deemed permanent TOTAL": "Which disabilities are deemed permanent TOTAL?",
 "Permanent partial disability (after 36 contributions): months of pension for loss of one hand / one arm / one foot / one leg": "Permanent partial disability (after 36 contributions): how many months of pension for the loss of one hand / one arm / one foot / one leg?",
 "Permanent partial disability: months of pension for one thumb / one index finger / one big toe / sight of one eye": "Permanent partial disability: how many months of pension for the loss of one thumb / one index finger / one big toe / sight of one eye?",
 "Permanent partial disability: months of pension for hearing of one ear / hearing of both ears / both ears": "Permanent partial disability: how many months of pension for the loss of hearing of one ear / hearing of both ears / both ears?",
 "Funeral benefit under RA 11199": "How much is the funeral benefit under RA 11199?",
 "Sickness benefit eligibility": "Who is eligible for the sickness benefit?",
 "Daily sickness benefit amount, and who pays it": "How much is the daily sickness benefit, and who pays it?",
 "Limits on the sickness benefit": "What are the limits on the sickness benefit?",
 "Unemployment insurance (involuntary separation) benefit": "Who qualifies for the unemployment insurance (involuntary separation) benefit, and how much is it?",
 "Examples of involuntary separation": "What are examples of involuntary separation?",
 "Penalty for failing to register employees or to deduct and remit contributions": "What is the penalty for failing to register employees or to deduct and remit contributions?",
 # ---- Labor Standards ----
 "Declaration of basic policy of the Labor Code": "What is the declared basic policy of the Labor Code?",
 "Prohibition against elimination or diminution of benefits": "What does the prohibition against elimination or diminution of benefits say?",
 "Labor standards": "What are labor standards?",
 "Basic pay (basic salary)": "What is basic pay (basic salary)?",
 "Primary mode the State promotes for settling wages and other terms of employment": "What is the primary mode the State promotes for settling wages and other terms of employment?",
 "Workers excepted from wage increases under wage orders": "Which workers are excepted from wage increases under wage orders?",
 "Holiday pay for an unworked regular holiday": "How much is the holiday pay for an unworked regular holiday, and on what condition?",
 "Pay for work on a regular holiday (first 8 hours)": "How much is the pay for work on a regular holiday (first 8 hours)?",
 "Double regular holiday: pay if unworked / if worked": "On a double regular holiday, how much is the pay if unworked / if worked?",
 "Employees excluded from holiday pay": "Which employees are excluded from holiday pay?",
 "Three conditions for a managerial employee to be excluded": "What are the three conditions for a managerial employee to be excluded?",
 "The regular holidays": "What are the regular holidays?",
 "Premium pay": "What is premium pay?",
 "Special (non-working) day, unworked": "What is the pay for an unworked special (non-working) day?",
 "Worked on a special (non-working) day that is also the rest day": "How much is the pay for work on a special (non-working) day that is also the rest day?",
 "Worked on a regular holiday that is also the rest day": "How much is the pay for work on a regular holiday that is also the rest day?",
 "Employees excluded from PREMIUM PAY": "Which employees are excluded from PREMIUM PAY?",
 "Field personnel": "Who are field personnel?",
 "Weekly rest day": "How long is the weekly rest day, and how often is it given?",
 "The regular special (non-working) days": "What are the regular special (non-working) days?",
 "Days traditionally declared as additional special (non-working) days": "Which days are traditionally declared as additional special (non-working) days?",
 "Normal hours of work": "What are the normal hours of work?",
 "Meal period the employer must give": "How long is the meal period the employer must give?",
 "Overtime on an ordinary working day": "What is the overtime pay on an ordinary working day?",
 "Overtime on a special day, rest day, or regular holiday": "What is the overtime pay on a special day, rest day, or regular holiday?",
 "Overtime rates: rest or special day / special day on rest day / regular holiday / regular holiday on rest day": "What are the overtime rates on a rest or special day / special day on rest day / regular holiday / regular holiday on rest day?",
 "Night shift differential": "What is the night shift differential?",
 "Night shift rates: ordinary day / rest or special day / regular holiday / regular holiday on rest day": "What are the night shift rates on an ordinary day / rest or special day / regular holiday / regular holiday on rest day?",
 "Ordinary day, night shift, overtime rate": "What is the rate for night shift overtime on an ordinary day?",
 "Double holiday rates: unworked-and-worked / on rest day / overtime": "What are the double holiday rates: unworked-and-worked / on rest day / overtime?",
 "13th month pay amount": "How much is the 13th month pay?",
 "Employers NOT covered by PD 851": "Which employers are NOT covered by PD 851?",
 "Deadline for paying the 13th month pay": "When is the deadline for paying the 13th month pay?",
 "Factors for converting a daily wage to an annual amount": "What factors convert a daily wage to an annual amount?",
 "Service incentive leave": "How many days is the service incentive leave, and who is entitled to it?",
 "Employees excluded from service incentive leave": "Which employees are excluded from service incentive leave?",
 "Maternity leave for live childbirth": "How long is maternity leave for live childbirth?",
 "Maternity leave for miscarriage or emergency termination of pregnancy": "How long is maternity leave for miscarriage or emergency termination of pregnancy?",
 "Compulsory postnatal leave": "How long is the compulsory postnatal leave?",
 "Emergency termination of pregnancy": "What is emergency termination of pregnancy?",
 "Conditions for maternity leave": "What are the conditions for maternity leave?",
 "Paternity leave": "How long is paternity leave, and for whom?",
 "Conditions for paternity leave": "What are the conditions for paternity leave?",
 "Meaning of \"cohabiting\" for paternity leave": "What does \"cohabiting\" mean for paternity leave?",
 "Parental leave for solo parents": "How long is the parental leave for solo parents?",
 "Conditions for parental leave of a solo parent": "What are the conditions for parental leave of a solo parent?",
 "Other solo parents under RA 11861": "Who else are solo parents under RA 11861?",
 "Age limit for the child or dependent of a solo parent": "What is the age limit for the child or dependent of a solo parent?",
}


def ask(front):
    """The question text shown for a card (second line = stem, if any)."""
    q = ASK.get(front)
    if q is None and front.startswith("The remuneration or earnings"):
        q = "What term is defined as: \"" + front[0].lower() + front[1:] + "\"?"
    q = q or front
    if front in STEM:
        q += "\n" + STEM[front]
    return q

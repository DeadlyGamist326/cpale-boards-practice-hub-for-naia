"""RFBT flashcards, built strictly from the topics in Naia's RFBT handouts (Social Security Law, Labor Standards), written as short Q&A of the rules with their legal sources. No handout prose or branding.
Each card: (front, back, source)."""
import html, json, hashlib

SSL = [
 # Policy and the SSS / Commission
 ("The Social Security Act of 2018 is Republic Act No. ___.", "11199", "RA 11199"),
 ("The value a social security program must emphasize under RA 11199", "\"Work, save, invest and prosper\"", "RA 11199, Sec. 2"),
 ("The hazards social security protects members against", "Disability, sickness, maternity, old age, death, and other contingencies resulting in loss of income or financial burden", "RA 11199, Sec. 2"),
 ("The SSS functions and operates as what kind of entity?", "An independent and accountable government-owned and -controlled corporation (GOCC), with principal place of business in Metro Manila", "RA 11199, Sec. 3"),
 ("Who directs and controls the SSS?", "The Social Security Commission", "RA 11199, Sec. 3"),
 ("Who is the ex officio Chairperson of the Social Security Commission?", "The Secretary of Finance", "RA 11199, Sec. 3"),
 ("Who is the Vice-Chairperson of the Social Security Commission?", "The SSS President and CEO, who acts as Chairperson when the Finance Secretary is absent", "RA 11199, Sec. 3"),
 ("Composition of the Social Security Commission (9 members)", "Secretary of Finance (Chair), SSS President and CEO (Vice-Chair), Secretary of Labor (ex officio), and 6 appointive members: 3 for workers and 3 for employers, each group with at least 1 woman", "RA 11199, Sec. 3"),
 ("Who appoints the six appointive Commission members, and how much experience must they have?", "The President of the Philippines; at least 10 years of managerial or leadership experience", "RA 11199, Sec. 3"),
 ("Term of office of the appointive Commission members", "3 years, extendable for another 3 years", "RA 11199, Sec. 3"),
 # Definitions
 ("Employer under RA 11199", "Any person, natural or juridical, domestic or foreign, who carries on in the Philippines any trade, business, industry, undertaking or activity and uses the services of another under his orders, EXCEPT the Government and its political subdivisions, branches, instrumentalities and GOCCs", "RA 11199, Sec. 8(c)"),
 ("Is a self-employed person an employee or an employer under RA 11199?", "Both at the same time", "RA 11199, Sec. 8(c), (d)"),
 ("Who are the dependents of a member?", "(1) Legal spouse entitled by law to support; (2) legitimate, legitimated, legally adopted, and illegitimate child who is unmarried, not gainfully employed, and below 21; (3) parent receiving regular support from the member", "RA 11199, Sec. 8(e)"),
 ("A child over 21 is still a dependent if ___.", "He or she is congenitally, or while still a minor became, permanently incapacitated and incapable of self-support, physically or mentally", "RA 11199, Sec. 8(e)"),
 ("Compensation under RA 11199", "All actual remuneration for employment, including the mandated COLA and the cash value of non-cash pay, EXCEPT the part received during the month in excess of the maximum salary credit", "RA 11199, Sec. 8(f)"),
 ("Monthly salary credit", "The compensation base for contributions and benefits. For computing benefits, the maximum MSC considered is ₱20,000 until adjusted.", "RA 11199, Sec. 8(g)"),
 ("Services EXCLUDED from \"employment\" under RA 11199", "(1) No employer-employee relationship; (2) employ of the Philippine Government; (3) employ of a foreign government or international organization or their wholly-owned instrumentality; (4) temporary and other employees excluded by Commission regulation", "RA 11199, Sec. 8(j)"),
 ("Are employees of bona fide independent contractors employees of the company that hires the contractor?", "No", "RA 11199, Sec. 8(j)"),
 ("Primary beneficiaries", "The dependent spouse until he or she remarries, and the dependent legitimate, legitimated, legally adopted, and illegitimate children", "RA 11199, Sec. 8(k)"),
 ("Share of dependent illegitimate children when there are legitimate children", "50% of the share of the legitimate, legitimated, or legally adopted children (100% if there are none)", "RA 11199, Sec. 8(k)"),
 ("Secondary beneficiaries", "The dependent parents, in the absence of primary beneficiaries; if none, any other person designated by the member", "RA 11199, Sec. 8(k)"),
 ("Contingencies under RA 11199", "Retirement, death, disability, injury or sickness, and maternity (the IRR adds unemployment or involuntary separation)", "RA 11199, Sec. 8(l)"),
 ("Average monthly salary credit (AMSC)", "The higher of: sum of the last 60 MSCs before the semester of contingency ÷ 60, OR sum of all MSCs paid before the semester ÷ number of monthly contributions paid", "RA 11199, Sec. 8(m)"),
 ("Average daily salary credit (ADSC)", "Sum of the 6 highest MSCs in the 12 months before the semester of contingency ÷ 180", "RA 11199, Sec. 8(n)"),
 ("Semester", "Two consecutive quarters ending in the quarter of contingency", "RA 11199, Sec. 8(o)"),
 ("Quarter", "Three consecutive calendar months ending on the last day of March, June, September, and December", "RA 11199, Sec. 8(p)"),
 ("Credited years of service for a member covered in or after January 1985", "The number of calendar years in which 6 or more contributions were paid, from the year of coverage up to the year containing the semester before the contingency", "RA 11199, Sec. 8(q)"),
 # Coverage
 ("Compulsory coverage applies to all employees, including kasambahays, not over ___ years of age, and their employers.", "60", "RA 11199, Sec. 9"),
 ("Spouses who devote full time to managing the household and family affairs may be covered on a ___ basis.", "Voluntary", "RA 11199, Sec. 9"),
 ("When does compulsory coverage take effect for the employer? For the employee?", "Employer: first day of operation. Employee: the day of employment.", "RA 11199, Sec. 10"),
 ("When a covered employee is separated, when do the employer's contribution obligations stop?", "At the end of the month of separation. The employee may continue paying the total contribution to keep full benefits.", "RA 11199, Sec. 10"),
 ("Self-employed persons who are compulsorily covered (examples)", "Self-employed professionals; partners and single proprietors; actors, directors, scriptwriters and news correspondents who are not employees; professional athletes, coaches, trainers and jockeys; individual farmers and fishermen", "RA 11199, Sec. 9-A"),
 ("When does coverage of a self-employed person take effect?", "Upon his or her registration with the SSS", "RA 11199, Sec. 9-A"),
 ("Must a self-employed member pay contributions for a month with no income?", "No", "RA 11199, Sec. 9-A"),
 ("Within how many days must a self-employed member register with the SSS?", "30 days from the first day of practice or business operations", "RA 11199, Sec. 11-A"),
 ("Whose contributions does a self-employed member pay?", "Both the employer and the employee contributions, based on the monthly earnings declared at registration", "RA 11199, Sec. 19-A"),
 ("Contributions of self-employed persons earning ___ a month or below may be reduced by the Commission.", "₱1,000", "RA 11199, Sec. 19-A"),
 ("Which OFWs are compulsorily covered?", "All sea-based and land-based OFWs not over 60 years of age", "RA 11199, Sec. 9-B"),
 ("Who is considered the employer of sea-based OFWs?", "The manning agencies, which are solidarily liable with their principals for civil liabilities", "RA 11199, Sec. 9-B"),
 ("How are land-based OFWs treated for SSS coverage?", "As compulsory members treated in the same manner as self-employed persons, unless a bilateral agreement makes their foreign employers pay", "RA 11199, Sec. 9-B"),
 ("How may Filipino permanent migrants and naturalized citizens of other countries be covered?", "On a voluntary basis", "RA 11199, Sec. 9-B"),
 # Records, contributions, remittance
 ("If a covered employee dies, gets sick or disabled, or reaches 60 before the employer reported him, the employer pays the SSS damages equal to ___.", "The benefits the employee would have received. For pensions: the accumulated pension or 5 years' pension, whichever is higher. No liability if the contingency happens within 30 days from employment.", "RA 11199, Sec. 24"),
 ("When must the Annual Register of New and Separated Employees be submitted?", "In January of each year", "RA 11199, Sec. 24"),
 ("Before issuing an annual business permit, an LGU must require ___.", "A certificate of SSS coverage and compliance, which the SSS must issue within 5 working days", "RA 11199, Sec. 24"),
 ("May an employer deduct its own SSS contribution from employees' pay?", "No, notwithstanding any contract to the contrary", "RA 11199, Sec. 19"),
 ("Deadline to remit SSS contributions", "Within the first 10 days of the calendar month following the month they apply to (or as the Commission prescribes)", "RA 11199, Sec. 22"),
 ("Penalty for late remittance of contributions", "2% per month from the date the contribution falls due until paid", "RA 11199, Sec. 22"),
 ("How are unpaid contributions collected when an employer refuses or neglects to pay?", "In the same manner as taxes under the NIRC; also by court action or by a warrant to the sheriff to levy and sell the debtor's property", "RA 11199, Sec. 22"),
 ("Does the employer's failure to remit contributions affect the employee's right to benefits?", "No", "RA 11199, Sec. 22"),
 ("Prescriptive period for action against an employer for unpaid contributions", "20 years from when the delinquency is known or the assessment is made, or from when the benefit accrues", "RA 11199, Sec. 22(b)"),
 ("SSS benefit payments are exempt from ___.", "All taxes, fees or charges, and from attachment, garnishment, levy or seizure, except to pay the member's debt to the SSS", "RA 11199, Sec. 16"),
 # Benefits
 ("Monthly pension: the highest of what three amounts?", "(1) ₱300 + 20% of AMSC + 2% of AMSC for each credited year of service beyond 10; (2) 40% of AMSC; (3) ₱1,000. Paid for no less than 60 months in total.", "RA 11199, Sec. 12"),
 ("Minimum monthly pension", "₱1,200 with at least 10 credited years of service; ₱2,400 with 20 credited years", "RA 11199, Sec. 12"),
 ("Additional benefit allowance for pensioners (from January 2017)", "₱1,000 a month for retirement, death and disability pensioners, separate from the pension; it does not cover the dependents' pension", "RA 11199, Sec. 12; IRR"),
 ("Dependents' pension", "10% of the monthly pension or ₱250, whichever is higher, for each dependent child conceived on or before the contingency, up to 5 children, starting with the youngest, without substitution. Legitimate children are preferred.", "RA 11199, Sec. 12-A"),
 ("Who qualifies for the retirement pension?", "A member with at least 120 monthly contributions before the semester of retirement who is 60 and separated from employment (or no longer self-employed), or who is 65", "RA 11199, Sec. 12-B"),
 ("How many monthly retirement pensions may the member choose to get in advance as a lump sum?", "The first 18, discounted at a preferential interest rate", "RA 11199, Sec. 12-B"),
 ("What happens to the pension of a retiree under 65 who is reemployed?", "It is suspended", "RA 11199, Sec. 12-B"),
 ("A member who is 60 at retirement but lacks 120 contributions gets ___.", "A lump sum equal to the total contributions paid by and for him, if separated and not continuing to pay", "RA 11199, Sec. 12-B"),
 ("A retiree with no primary beneficiaries dies within 60 months of starting his pension. The secondary beneficiaries get ___.", "A lump sum equal to the pensions for the rest of the 5-year guaranteed period, excluding dependents' pension", "RA 11199, Sec. 12-B"),
 ("Death benefit when the member paid at least 36 monthly contributions before the semester of death", "Monthly pension to the primary beneficiaries; if none, the secondary beneficiaries get a lump sum of 36 times the monthly pension", "RA 11199, Sec. 13"),
 ("Death benefit when the member paid FEWER than 36 monthly contributions", "Lump sum to primary or secondary beneficiaries: the higher of the monthly pension × number of contributions paid, or 12 × the monthly pension", "RA 11199, Sec. 13"),
 ("Permanent total disability benefit with at least 36 monthly contributions before the semester of disability", "Monthly pension", "RA 11199, Sec. 13-A"),
 ("Permanent total disability benefit with FEWER than 36 contributions", "Lump sum: the higher of the monthly pension × number of contributions paid, or 12 × the monthly pension", "RA 11199, Sec. 13-A"),
 ("A disabled member who got a lump sum and is reemployed not earlier than ___ from the disability becomes a new member.", "1 year", "RA 11199, Sec. 13-A"),
 ("Disabilities deemed permanent TOTAL", "Complete loss of sight of both eyes; loss of two limbs at or above the ankle or wrists; permanent complete paralysis of two limbs; brain injury resulting in incurable imbecility or insanity; other cases approved by the SSS", "RA 11199, Sec. 13-A"),
 ("When are the disability pension and dependents' pension suspended?", "On reemployment or resumption of self-employment, recovery from the disability, or failure to appear for examination at least once a year when notified", "RA 11199, Sec. 13-A"),
 ("Permanent partial disability (after 36 contributions): months of pension for loss of one hand / one arm / one foot / one leg", "39 / 50 / 31 / 46 months", "RA 11199, Sec. 13-A"),
 ("Permanent partial disability: months of pension for one thumb / one index finger / one big toe / sight of one eye", "10 / 8 / 6 / 25 months", "RA 11199, Sec. 13-A"),
 ("Permanent partial disability: months of pension for hearing of one ear / hearing of both ears / both ears", "10 / 50 / 20 months", "RA 11199, Sec. 13-A"),
 ("When is a permanent partial disability pension paid in a lump sum?", "When it is payable for less than 12 months", "RA 11199, Sec. 13-A"),
 ("Funeral benefit under RA 11199", "₱12,000, in cash or in kind (the IRR now sets a variable ₱20,000 to ₱40,000 effective August 1, 2015)", "RA 11199, Sec. 13-B; IRR"),
 ("Sickness benefit eligibility", "At least 3 monthly contributions in the 12 months before the semester of sickness or injury, and confinement for MORE than 3 days in a hospital or elsewhere with SSS approval", "RA 11199, Sec. 14"),
 ("Daily sickness benefit amount, and who pays it", "90% of the average daily salary credit; paid by the employer (or by the SSS if unemployed or self-employed)", "RA 11199, Sec. 14"),
 ("Limits on the sickness benefit", "Not more than 120 days in one calendar year (unused days do not carry over), and not more than 240 days for the same confinement", "RA 11199, Sec. 14"),
 ("Within how many days must the employee notify the employer of sickness?", "5 calendar days after confinement starts. Not needed if confined in a hospital or if sick or injured while working or on the employer's premises.", "RA 11199, Sec. 14"),
 ("When does the sickness allowance begin to be paid?", "Only after all sick leaves with full pay credited to the employee are used up", "RA 11199, Sec. 14"),
 ("Unemployment insurance (involuntary separation) benefit", "For a member not over 60 with at least 36 monthly contributions, 12 of them in the 18 months before separation: 50% of AMSC monthly for up to 2 months, claimable once every 3 years", "RA 11199, Sec. 14-B"),
 ("Examples of involuntary separation", "Installation of labor-saving devices, redundancy, retrenchment to prevent loss, closure or cessation of operation, disease or illness", "IRR-SSS, Rule 27"),
 ("If two or more compensable contingencies occur at the same time, ___.", "Only the highest benefit is paid", "RA 11199, Sec. 14-B"),
 # Penal clauses
 ("Penalty for failing to register employees or to deduct and remit contributions", "Fine of ₱5,000 to ₱20,000 AND imprisonment of 6 years and 1 day to 12 years", "RA 11199, Sec. 28"),
 ("If an association, partnership or corporation violates RA 11199, who is liable?", "Its managing head, directors, or partners", "RA 11199, Sec. 28"),
 ("Making false statements to obtain SSS benefits or loans is penalized under ___ of the Revised Penal Code.", "Article 172 (falsification by private individual)", "RA 11199, Sec. 28"),
 ("An SSS employee who misappropriates SSS funds suffers the penalties under ___ of the Revised Penal Code.", "Article 217 (malversation)", "RA 11199, Sec. 28"),
]

LABOR = [
 # Policies and basic concepts
 ("The Labor Code of the Philippines is Presidential Decree No. ___.", "442, as amended", "PD 442"),
 ("Declaration of basic policy of the Labor Code", "The State shall afford protection to labor, promote full employment, ensure equal work opportunities regardless of sex, race or creed, and regulate the relations between workers and employers", "Labor Code, Art. 3"),
 ("How are doubts in interpreting the Labor Code and its rules resolved?", "In favor of labor", "Labor Code, Art. 4"),
 ("Prohibition against elimination or diminution of benefits", "Nothing in the Code shall be construed to eliminate or diminish supplements or other employee benefits being enjoyed when the Code was promulgated", "Labor Code, Art. 100"),
 ("Labor standards", "The minimum requirements prescribed by laws and rules on wages, hours of work, COLA and other monetary and welfare benefits, including occupational safety and health standards", "Ceprado v. Nationwide Security (2015)"),
 ("Are \"wage\", \"salary\", and \"pay\" different in meaning?", "No. They are essentially synonymous: a reward or recompense for services performed.", "Songco v. NLRC (1990)"),
 ("The remuneration or earnings, however designated, capable of being expressed in terms of money, whether fixed or ascertained on a time, task, piece, or commission basis, or other method of calculating the same, payable by an employer to an employee under a written or unwritten contract of employment for work done or to be done, or for services rendered or to be rendered", "Wage", "Labor Code, Art. 97(f)"),
 ("Besides money, wage also includes ___.", "The fair and reasonable value, as determined by the Secretary of Labor, of board, lodging, or other facilities customarily furnished by the employer. It must not include any profit to the employer.", "Labor Code, Art. 97(f)"),
 ("Basic pay (basic salary)", "The rate of pay for a standard work period, excluding additional payments such as bonuses and overtime", "Boie-Takeda v. De la Serna (1993)"),
 ("Primary mode the State promotes for settling wages and other terms of employment", "Collective bargaining", "Labor Code"),
 ("Who prescribes the regional minimum wage rates?", "The Regional Tripartite Wages and Productivity Boards", "Labor Code, Arts. 99, 122"),
 ("Can a wage order stop workers from bargaining for higher wages?", "No", "Labor Code, Art. 125"),
 ("Workers excepted from wage increases under wage orders", "Workers of duly registered Barangay Micro Business Enterprises (BMBEs) with a Certificate of Authority (RA 10644)", "RA 10644"),
 # Holiday pay
 ("Holiday pay for an unworked regular holiday", "At least 100% of the daily wage, provided the employee is present or on paid leave on the workday immediately before the holiday", "Labor Code, Art. 94"),
 ("Pay for work on a regular holiday (first 8 hours)", "At least 200% of the regular daily wage", "IRR, Rule IV, Sec. 4"),
 ("Double regular holiday: pay if unworked / if worked", "200% / 300% of the daily wage", "DOLE Handbook"),
 ("Which establishments are exempt from HOLIDAY PAY because of size?", "Retail and service establishments regularly employing fewer than 10 workers", "DOLE Handbook"),
 ("Employees excluded from holiday pay", "Government employees; retail and service workers in establishments with fewer than 10 workers; kasambahay and persons in personal service; managerial employees; officers or members of the managerial staff; field personnel and others whose time and performance are unsupervised (task, contract, purely commission, or fixed-amount basis)", "DOLE Handbook"),
 ("Three conditions for a managerial employee to be excluded", "(1) Primary duty is to manage the establishment or a department; (2) customarily directs the work of 2 or more employees; (3) can hire or fire, or their recommendations on hiring, firing and promotion are given particular weight", "DOLE Handbook"),
 ("Officers or members of the managerial staff may not spend more than ___ of their weekly hours on work not closely related to their managerial duties.", "20%", "DOLE Handbook"),
 ("The regular holidays", "New Year's Day, Maundy Thursday, Good Friday, Eidul Fitr, Eidul Adha, Araw ng Kagitingan, Labor Day, Independence Day, National Heroes Day, Bonifacio Day, Christmas Day, Rizal Day", "EO 292, as amended by RA 9849"),
 ("When are National Heroes Day and Araw ng Kagitingan observed?", "National Heroes Day: last Monday of August. Araw ng Kagitingan: Monday nearest April 9.", "RA 9849"),
 ("An employee on leave WITHOUT pay the day before a regular holiday, who does not work on the holiday, gets ___.", "May not be paid holiday pay", "IRR, Rule IV, Sec. 6"),
 ("The day before the holiday is a rest day or non-workday. When is the employee entitled to holiday pay?", "If he or she worked on the day immediately before that rest day or non-workday", "IRR, Rule IV, Sec. 6"),
 ("Two successive regular holidays (e.g., Maundy Thursday and Good Friday): an employee absent the day before the first holiday is paid ___.", "Not for both holidays, unless he or she works on the first holiday, in which case he or she gets holiday pay on the second", "IRR, Rule IV, Sec. 10"),
 # Premium pay and rest days
 ("Premium pay", "Additional compensation for work within 8 hours on rest days and special days", "Labor Code, Arts. 91–93"),
 ("Special (non-working) day, unworked", "\"No work, no pay\", unless a favorable company policy, practice, or CBA grants pay", "DOLE Handbook"),
 ("If employee worked on a special (non-working) day, the employee shall be paid an additional ___ of the basic wage on the first eight hours of work.", "30% (130% of the regular daily wage)", "DOLE Handbook"),
 ("Worked on a special (non-working) day that is also the rest day", "Additional 50% of the basic wage (150%)", "DOLE Handbook"),
 ("Worked on a regular holiday that is also the rest day", "Additional 30% on the 200% basic wage (260%)", "DOLE Handbook"),
 ("Employees excluded from PREMIUM PAY", "Government employees; kasambahay and persons in personal service; managerial employees; managerial staff; workers paid by results (piece rate, takay, pakyaw, task); field personnel", "DOLE Handbook"),
 ("Field personnel", "Employees who regularly work away from the principal or branch office and whose actual hours in the field cannot be determined with reasonable certainty", "DOLE Handbook"),
 ("Weekly rest day", "At least 24 consecutive hours after every 6 consecutive normal work days", "IRR, Rule III, Secs. 3–4"),
 ("Who schedules the weekly rest day, and whose preference must be respected?", "The employer, subject to the CBA and DOLE rules; the employee's preference must be respected if based on religious grounds", "IRR, Rule III, Sec. 4"),
 ("When may an employer require work on the scheduled rest day?", "Actual or impending emergencies (accident, fire, flood, typhoon, earthquake, epidemic) to prevent loss of life or property; urgent work on machinery to avoid serious loss; abnormal pressure of work; to prevent loss of perishable goods; continuous operations where stoppage causes irreparable loss; analogous cases set by DOLE", "IRR, Rule III, Sec. 6"),
 ("The regular special (non-working) days", "Ninoy Aquino Day (Aug 21), All Saints' Day (Nov 1), Feast of the Immaculate Conception (Dec 8), Last Day of the Year (Dec 31)", "EO 292, as amended; RA 10966"),
 ("Days traditionally declared as additional special (non-working) days", "Chinese New Year, Black Saturday, All Souls' Day (Nov 2), Christmas Eve (Dec 24)", "Handout"),
 # Overtime and NSD
 ("Normal hours of work", "Not more than 8 hours a day", "Labor Code, Art. 83"),
 ("Hours worked include ___.", "(a) All time the employee must be on duty or at a prescribed workplace; (b) all time the employee is suffered or permitted to work", "Labor Code, Art. 84"),
 ("Meal period the employer must give", "Not less than 60 minutes time-off for regular meals", "Labor Code, Art. 85"),
 ("Can undertime on one day offset overtime on another day?", "No. Permission to take leave on another day also does not excuse paying the overtime.", "Labor Code, Art. 88"),
 ("Overtime on an ordinary working day", "Additional 25% of the hourly rate (125%)", "Labor Code, Art. 87"),
 ("Overtime on a special day, rest day, or regular holiday", "Additional 30% of the hourly rate ON THAT DAY (e.g., 130% × 130% = 169% on a rest day)", "Labor Code, Art. 87"),
 ("Overtime rates: rest or special day / special day on rest day / regular holiday / regular holiday on rest day", "169% / 195% / 260% / 338% of the hourly rate", "DOLE Handbook"),
 ("When may an employer require compulsory overtime?", "War or declared emergency; to prevent loss of life or property or danger to public safety; urgent work on machines; to prevent loss of perishable goods; to finish work started before the 8th hour to prevent serious obstruction; to take advantage of favorable weather", "IRR; Labor Code, Art. 89"),
 ("Night shift differential", "Additional 10% of the hourly rate for work between 10:00 PM and 6:00 AM (110%)", "Labor Code, Art. 86"),
 ("Which establishments are exempt from NIGHT SHIFT DIFFERENTIAL because of size?", "Retail and service establishments regularly employing fewer than FIVE (5) workers", "DOLE Handbook"),
 ("Night shift rates: ordinary day / rest or special day / regular holiday / regular holiday on rest day", "110% / 143% / 220% / 286% of the hourly rate", "DOLE Handbook"),
 ("Ordinary day, night shift, overtime rate", "1 × 1.1 × 1.25 = 137.5% of the hourly rate", "DOLE Handbook"),
 ("Double holiday rates: unworked-and-worked / on rest day / overtime", "300% / 390% / 390% (3 × 1.3)", "DOLE Handbook"),
 ("How do you get the hourly rate for OT and NSD?", "Daily wage ÷ 8 hours", "DOLE Handbook"),
 # 13th month
 ("13th month pay amount", "Not less than 1/12 of the total basic salary earned in a calendar year", "PD 851 IRR"),
 ("What is EXCLUDED from basic salary for the 13th month pay?", "Cash equivalent of unused vacation and sick leave, overtime, premium, night shift differential, holiday pay, and COLA (unless treated as part of basic salary by agreement, practice or policy)", "PD 851 IRR"),
 ("Who are entitled to 13th month pay?", "All rank-and-file employees, regardless of the nature of employment or how paid, who worked at least 1 month in the calendar year", "PD 851 IRR"),
 ("Employers NOT covered by PD 851", "Government and its subdivisions (except GOCCs operating as private subsidiaries); employers already paying a 13th month or more when PD 851 was issued; employers of household helpers and persons in personal service; employers of workers paid purely on commission, boundary or task basis, or a fixed amount for specific work (but piece-rate workers ARE covered)", "PD 851 IRR"),
 ("Is a kasambahay entitled to 13th month pay?", "Yes, under the Batas Kasambahay (RA 10361, Sec. 25)", "RA 10361"),
 ("Deadline for paying the 13th month pay", "Not later than December 24", "PD 851"),
 ("Factors for converting a daily wage to an annual amount", "365 for monthly-paid employees; 313 for daily-paid employees not paid on rest days", "DOLE Handbook"),
 # Leaves
 ("Service incentive leave", "5 days with pay every year, for an employee with at least 1 year of service", "Labor Code, Art. 95"),
 ("\"At least one year of service\" means ___.", "At least 12 months, continuous or broken, from the start of work, including authorized absences and paid regular holidays (or a shorter period if that is the company's working year)", "IRR, Rule V, Sec. 3"),
 ("What happens to unused service incentive leave?", "It is commuted to cash at the end of the year; if never used or commuted, it is paid upon resignation or separation, at the salary rate on the date of commutation", "IRR, Rule V, Sec. 5"),
 ("Employees excluded from service incentive leave", "Government employees; persons in personal service; managerial employees and managerial staff; field personnel and unsupervised workers; those already enjoying the benefit; those with at least 5 days paid vacation leave; employees of establishments regularly employing fewer than 10", "DOLE Handbook"),
 ("Are vacation and sick leaves mandated by law?", "No. The law mandates the 5-day service incentive leave, which may be used for sick, vacation, or other purposes.", "Labor Code, Art. 95"),
 ("Maternity leave for live childbirth", "105 days with full pay; +15 days with full pay for a solo parent; an optional extra 30 days WITHOUT pay with due notice to the employer", "RA 11210"),
 ("Maternity leave for miscarriage or emergency termination of pregnancy", "60 days with full pay", "RA 11210"),
 ("Compulsory postnatal leave", "Not less than 60 days, within the 105 days", "RA 11210"),
 ("Emergency termination of pregnancy", "Pregnancy loss on or after the 20th week of gestation, including stillbirth", "IRR-EMLL"),
 ("Who are covered by the Expanded Maternity Leave Law?", "Female workers in the public sector, private sector, and informal economy; female voluntary SSS contributors; female national athletes, regardless of civil status, employment status, or the child's legitimacy", "IRR-EMLL"),
 ("Conditions for maternity leave", "At least 3 monthly SSS contributions in the 12 months before the semester of childbirth, miscarriage or emergency termination, and notice to the employer (or SSS) of the pregnancy and probable delivery date", "IRR-EMLL"),
 ("How many maternity leave days may the mother allocate to the child's father?", "Up to 7 days, whether or not they are married; this is on top of paternity leave", "RA 11210"),
 ("If the father is dead, absent, or incapacitated, the mother may allocate leave to ___.", "An alternate caregiver: a relative within the 4th degree of consanguinity, or her current partner sharing the household, regardless of sexual orientation or gender identity", "RA 11210"),
 ("Can maternity leave be allocated in case of miscarriage or emergency termination?", "No", "RA 11210"),
 ("Paternity leave", "7 days with full pay for the first 4 deliveries of the legitimate spouse with whom the married male employee is cohabiting", "RA 8187"),
 ("Conditions for paternity leave", "Employee at the time of delivery; cohabiting with the spouse when she gives birth or miscarries; applied within a reasonable time (not required for miscarriage); the wife has given birth or miscarried", "RA 8187 IRR"),
 ("Is unused paternity leave convertible to cash?", "No", "RA 8187"),
 ("Meaning of \"cohabiting\" for paternity leave", "The obligation of husband and wife to live together; still entitled even if apart because of work", "DOLE Handbook"),
 ("Parental leave for solo parents", "Not more than 7 working days with pay every year, forfeitable and non-cumulative, for a solo parent with at least 6 months of service", "RA 8972, as amended by RA 11861"),
 ("Is unused solo parent leave convertible to cash?", "No, unless the employer and employee agreed on it beforehand", "RA 11861"),
 ("Conditions for parental leave of a solo parent", "At least 6 months of service (continuous or broken); notice to the employer within a reasonable time; a valid Solo Parent ID Card", "IRR-ESPWA"),
 ("Who are solo parents? (sole care of the child due to the spouse's ___)", "Death; detention of at least 3 months or serving sentence; physical or mental incapacity; legal or de facto separation of at least 6 months; nullity, annulment, or divorce; abandonment of at least 6 months. Also: a mother of a child born of rape", "RA 11861, Sec. 4"),
 ("Other solo parents under RA 11861", "Spouse, family member or guardian of a low/semi-skilled OFW away for 12 uninterrupted months; unmarried mother or father who keeps the child; sole legal guardian, adoptive or foster parent; relative within the 4th degree who assumed sole care for at least 6 months; a pregnant woman with sole care of the unborn child", "RA 11861, Sec. 4"),
 ("Age limit for the child or dependent of a solo parent", "22 years old or below (or older if unable to care for themselves due to disability)", "IRR-ESPWA"),
]

DECKS = [("ssl", "Social Security Law", "RA 11199: the SSS, definitions, coverage, contributions, benefits, penalties", SSL),
         ("labor", "Labor Standards", "Wages, holiday and premium pay, overtime, night shift, 13th month pay, leaves", LABOR)]

CSS = """
.fcv h2{margin-bottom:4px}
.fchint{color:var(--muted);margin:0 0 14px}
.card{display:flex;flex-direction:column;justify-content:center;gap:10px;width:100%;min-height:260px;border:2px solid var(--line);border-radius:16px;background:var(--soft);padding:22px 20px;text-align:center;font-family:Arial,Helvetica,sans-serif;font-size:19px;line-height:1.5;color:var(--ink)}
.card.flipped{background:var(--pink);border-color:var(--rose)}
.card .side{font-size:12px;font-weight:bold;text-transform:uppercase;letter-spacing:.1em;color:var(--muted)}
.card .fa{font-weight:bold;color:var(--deep);font-size:21px}
.card .src{font-size:13px;color:var(--muted)}
.card .mini{font-size:13px;line-height:1.4;color:var(--muted);border:1px dashed var(--line);border-radius:8px;padding:6px 8px;background:rgba(255,255,255,.6)}
.fcbar{display:flex;gap:8px;justify-content:space-between;align-items:center;margin:14px 0}
.fcbar button{font-size:15px;font-weight:bold;background:var(--bg);color:var(--deep);border:1.5px solid var(--rose);border-radius:8px;padding:10px 14px}
.fcbar .flip{background:var(--rose);color:#ffffff;flex:1}
.fcmeta{display:flex;justify-content:space-between;align-items:center;color:var(--muted);font-size:14px;font-variant-numeric:tabular-nums}
.fcmeta button{background:none;border:0;color:var(--rose);font-weight:bold;font-size:14px;padding:4px 0}
.showcrop{display:block;width:100%;margin-top:10px;font-size:15px;font-weight:bold;background:var(--bg);color:var(--deep);border:1.5px dashed var(--rose);border-radius:8px;padding:10px}
.crop{margin:10px 0 0;border:1.5px solid var(--rose);border-radius:12px;padding:8px;background:#ffffff}
.crop img{display:block;width:100%;height:auto}
.crop figcaption{font-size:13px;color:var(--muted);margin-top:6px;text-align:center}
.croptools{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;margin-top:18px;font-size:14px;color:var(--muted)}
.croptools .cl{cursor:pointer;color:var(--deep);font-weight:bold;border:1.5px solid var(--rose);border-radius:8px;padding:7px 12px}
.fclist{margin-top:22px}
.fclist summary{cursor:pointer;font-weight:bold;color:var(--deep)}
.fclist ol{padding-left:22px}
.fclist li{margin-bottom:10px}
.fclist .a{display:block;color:var(--deep);font-weight:bold}
@media (max-width:600px){.card{font-size:20px;min-height:300px}.card .fa{font-size:22px}.fcbar button{font-size:17px;padding:12px 14px}}
"""

JS = r"""
const CROPS={map:{},ready:null};
function idb(){return new Promise((res,rej)=>{try{const r=indexedDB.open("hubcrops",1);r.onupgradeneeded=()=>r.result.createObjectStore("kv");r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error)}catch(e){rej(e)}})}
function cropsLoad(){if(!CROPS.ready)CROPS.ready=idb().then(db=>new Promise(res=>{const t=db.transaction("kv").objectStore("kv").get("crops");t.onsuccess=()=>{CROPS.map=t.result||{};res()};t.onerror=()=>res()})).catch(()=>{});return CROPS.ready}
function cropsSave(m){CROPS.map=m;return idb().then(db=>new Promise(res=>{const tx=db.transaction("kv","readwrite");tx.objectStore("kv").put(m,"crops");tx.oncomplete=res;tx.onerror=res})).catch(()=>{})}
function initDeck(el){
  if(!el||el.dataset.ok)return;el.dataset.ok=1;
  const cards=JSON.parse(el.querySelector("script.deck").textContent),key="deck-"+el.id;
  let order=cards.map((_,i)=>i),i=0,back=false;
  try{const s=JSON.parse(localStorage.getItem(key)||"null");if(s&&s.order&&s.order.length===cards.length){order=s.order;i=s.i||0}}catch(e){}
  const card=el.querySelector(".card"),cnt=el.querySelector(".cnt"),slug=el.id.slice(3);
  const sc=el.querySelector(".showcrop"),fig=el.querySelector(".crop"),cst=el.querySelector(".cstat"),hov=matchMedia("(hover: hover)").matches;
  let open=false;
  function cropFor(){return back?CROPS.map[slug+":"+cards[order[i]][3]]:null}
  function paintCrop(){const c=cropFor();
    if(!c){sc.hidden=true;fig.hidden=true;return}
    fig.querySelector("img").src=c.img;fig.querySelector("figcaption").textContent=c.ref;
    sc.hidden=hov;fig.hidden=!open;sc.textContent=open?"Hide handout excerpt":"Show where it is in the handout"}
  function stat(){const n=Object.keys(CROPS.map).filter(k=>k.startsWith(slug+":")).length;cst.textContent=n?n+" handout crops loaded on this device":"No crops loaded on this device"}
  sc.onclick=()=>{open=!open;paintCrop()};
  if(hov){card.addEventListener("mouseenter",()=>{if(cropFor()){open=true;paintCrop()}});
    const out=e=>{const t=e.relatedTarget;if(t&&(card.contains(t)||fig.contains(t)))return;open=false;paintCrop()};
    card.addEventListener("mouseleave",out);fig.addEventListener("mouseleave",out)}
  el.querySelector(".fcload").onchange=e=>{const f=e.target.files[0];if(!f)return;const r=new FileReader();
    r.onload=()=>{try{const d=JSON.parse(r.result);if(d.kind!=="rfbt-crops")throw 0;cropsSave(Object.assign({},CROPS.map,d.crops)).then(()=>{stat();paintCrop()});cst.textContent="Loading…"}catch(x){cst.textContent="That file is not a crops file."}};r.readAsText(f)};
  cropsLoad().then(()=>{stat();paintCrop()});
  const esc=t=>t.replace(/&/g,"&amp;").replace(/</g,"&lt;");
  const seen=new Set();
  function draw(){const c=cards[order[i]];card.classList.toggle("flipped",back);if(back)seen.add(order[i]);
    card.innerHTML=back?'<span class="mini">'+esc(c[0])+'</span><span class="side">Answer</span><span class="fa">'+esc(c[1])+'</span><span class="src">'+esc(c[2])+'</span>'
                       :'<span class="side">Question</span><span>'+esc(c[0])+'</span>'+(seen.has(order[i])?'<span class="mini">'+esc(c[1])+'</span>':'<span class="src">Tap to show the answer</span>');
    cnt.textContent=(i+1)+" / "+cards.length;open=hov&&back&&card.matches(":hover");paintCrop();try{localStorage.setItem(key,JSON.stringify({order,i}))}catch(e){}}
  const go=d=>{i=(i+d+cards.length)%cards.length;back=false;draw()};
  card.onclick=()=>{back=!back;draw()};
  el.querySelector(".flip").onclick=()=>{back=!back;draw()};
  el.querySelector(".prev").onclick=()=>go(-1);
  el.querySelector(".next").onclick=()=>go(1);
  el.querySelector(".shuf").onclick=()=>{for(let k=order.length-1;k>0;k--){const j=Math.floor(Math.random()*(k+1));[order[k],order[j]]=[order[j],order[k]]}i=0;back=false;draw()};
  el.querySelector(".rst").onclick=()=>{order=cards.map((_,k)=>k);i=0;back=false;draw()};
  document.addEventListener("keydown",e=>{if(el.hidden)return;if(e.key==="ArrowRight")go(1);else if(e.key==="ArrowLeft")go(-1);else if(e.key===" "&&e.target===document.body){e.preventDefault();back=!back;draw()}});
  draw();
}
"""

def render():
    boxes, views = [], []
    for slug, title, blurb, cards in DECKS:
        boxes.append(f'<a class="sec xl" href="#fc-{slug}"><b>{title}</b>{blurb}<small>{len(cards)} flashcards</small></a>')
        data = json.dumps([list(c) + [hashlib.sha1(c[0].encode("utf-8")).hexdigest()[:12]] for c in cards], ensure_ascii=False).replace("</", "<\\/")
        lst = "".join(f'<li>{html.escape(f)}<span class="a">{html.escape(b)}</span></li>' for f, b, _ in cards)
        views.append(f'''<div class="fcv" id="fc-{slug}" hidden><div class="bar"><button type="button" class="back" data-home>← Home</button></div>
<p class="crumb">RFBT</p><h2>{title}</h2><p class="fchint">Tap the card to flip it. Use Next and Back to move through the deck.</p>
<button type="button" class="card" aria-live="polite"></button>
<button type="button" class="showcrop" hidden>Show where it is in the handout</button>
<figure class="crop" hidden><img alt="Handout excerpt"><figcaption></figcaption></figure>
<div class="fcbar"><button type="button" class="prev">← Back</button><button type="button" class="flip">Flip</button><button type="button" class="next">Next →</button></div>
<div class="fcmeta"><span class="cnt"></span><span><button type="button" class="shuf">Shuffle</button> · <button type="button" class="rst">Start over</button></span></div>
<div class="croptools"><label class="cl" for="fcload-{slug}">Load handout crops</label><input type="file" id="fcload-{slug}" class="fcload" accept=".json,application/json" hidden><span class="cstat"></span></div>
<details class="fclist"><summary>See all {len(cards)} cards</summary><ol>{lst}</ol></details>
<script type="application/json" class="deck">{data}</script></div>''')
    return "".join(boxes), "".join(views)

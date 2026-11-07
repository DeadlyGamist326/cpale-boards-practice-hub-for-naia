"""Hand-picked keywords per flashcard (user request: keywords must cue the answer, e.g. "minimum requirements").
Keyed by card front (the card ID). Each phrase is bolded wherever it appears, case-insensitive: on the question side
(including the STEM line) and in the answer. Phrases already bold are left alone."""

KEYS = {
 'The Social Security Act of 2018 is Republic Act No. ___.':
   'Republic Act No.',
 'The value a social security program must emphasize under RA 11199':
   'value|emphasize',
 'The hazards social security protects members against':
   'hazards|protect|Disability|sickness|maternity|old age|death|loss of income|financial burden',
 'The SSS functions and operates as what kind of entity?':
   'what kind of entity|independent|accountable|government-owned and -controlled corporation|GOCC|Metro Manila',
 'Who directs and controls the SSS?':
   'directs and controls',
 'Who is the ex officio Chairperson of the Social Security Commission?':
   'ex officio',
 'Who is the Vice-Chairperson of the Social Security Commission?':
   'acts as Chairperson',
 'Who appoints the six appointive Commission members, and how much experience must they have?':
   'Who appoints|experience|President of the Philippines|10 years|managerial or leadership experience',
 'Term of office of the appointive Commission members':
   'term of office|extendable',
 'Employer under RA 11199':
   'natural or juridical|domestic or foreign',
 'Is a self-employed person an employee or an employer under RA 11199?':
   'self-employed|employee or an employer',
 'Who are the dependents of a member?':
   'dependents',
 'A child over 21 is still a dependent if ___.':
   'over 21|still a dependent|congenitally|while still a minor|permanently incapacitated|incapable of self-support',
 'Compensation under RA 11199':
   'actual remuneration',
 'Monthly salary credit':
   'monthly salary credit|maximum MSC|compensation base|contributions and benefits',
 'Services EXCLUDED from "employment" under RA 11199':
   'EXCLUDED|No employer-employee relationship|Philippine Government|foreign government|international organization|temporary',
 'Are employees of bona fide independent contractors employees of the company that hires the contractor?':
   'bona fide independent contractors|company that hires',
 'Share of dependent illegitimate children when there are legitimate children':
   'illegitimate children|legitimate children|share of the legitimate',
 'Secondary beneficiaries':
   'secondary beneficiaries|dependent parents|absence of primary beneficiaries|designated by the member',
 'Contingencies under RA 11199':
   'contingencies|Retirement|death|disability|injury or sickness|maternity|unemployment or involuntary separation',
 'Average daily salary credit (ADSC)':
   'average daily salary credit|6 highest MSCs|12 months|÷ 180',
 'Semester':
   'semester|Two consecutive quarters|quarter of contingency',
 'Quarter':
   'quarter|Three consecutive calendar months|March, June, September, and December',
 'Credited years of service for a member covered in or after January 1985':
   'credited years of service|January 1985|calendar years|6 or more contributions',
 'Compulsory coverage applies to all employees, including kasambahays, not over ___ years of age, and their employers.':
   'Compulsory coverage|not over',
 'Spouses who devote full time to managing the household and family affairs may be covered on a ___ basis.':
   'managing the household',
 "When a covered employee is separated, when do the employer's contribution obligations stop?":
   'separated|contribution obligations stop|end of the month of separation|continue paying',
 'Self-employed persons who are compulsorily covered (examples)':
   'compulsorily covered|professionals|partners and single proprietors|actors, directors, scriptwriters|news correspondents|athletes|farmers and fishermen',
 'When does coverage of a self-employed person take effect?':
   'self-employed|take effect|registration',
 'Must a self-employed member pay contributions for a month with no income?':
   'no income',
 'Within how many days must a self-employed member register with the SSS?':
   'register|first day of practice or business operations',
 'Whose contributions does a self-employed member pay?':
   'Whose contributions|Both the employer and the employee|monthly earnings declared',
 'Contributions of self-employed persons earning ___ a month or below may be reduced by the Commission.':
   'reduced',
 'Which OFWs are compulsorily covered?':
   'OFWs|compulsorily covered|sea-based|land-based|not over 60',
 'Who is considered the employer of sea-based OFWs?':
   'employer of sea-based OFWs|manning agencies|solidarily liable',
 'How are land-based OFWs treated for SSS coverage?':
   'land-based OFWs|compulsory members|self-employed persons|bilateral agreement',
 'How may Filipino permanent migrants and naturalized citizens of other countries be covered?':
   'permanent migrants|naturalized citizens|voluntary',
 'If a covered employee dies, gets sick or disabled, or reaches 60 before the employer reported him, the employer pays the SSS damages equal to ___.':
   "before the employer reported him|damages|benefits the employee would have received|accumulated pension|5 years' pension|whichever is higher|No liability|30 days",
 'When must the Annual Register of New and Separated Employees be submitted?':
   'Annual Register',
 'Before issuing an annual business permit, an LGU must require ___.':
   'annual business permit|LGU|certificate of SSS coverage and compliance|5 working days',
 "May an employer deduct its own SSS contribution from employees' pay?":
   'deduct its own|contract to the contrary',
 'Deadline to remit SSS contributions':
   'deadline|first 10 days|month following',
 'Penalty for late remittance of contributions':
   'penalty|late remittance|2% per month|falls due',
 'How are unpaid contributions collected when an employer refuses or neglects to pay?':
   'refuses or neglects',
 "Does the employer's failure to remit contributions affect the employee's right to benefits?":
   'failure to remit|right to benefits',
 'Prescriptive period for action against an employer for unpaid contributions':
   'prescriptive period|20 years|delinquency is known|assessment is made|benefit accrues',
 'SSS benefit payments are exempt from ___.':
   'exempt',
 'Monthly pension: the highest of what three amounts?':
   'highest|three amounts',
 'Minimum monthly pension':
   'minimum monthly pension|credited years|10 credited years|20 credited years',
 'How many monthly retirement pensions may the member choose to get in advance as a lump sum?':
   'in advance|lump sum|first 18|preferential interest rate',
 'What happens to the pension of a retiree under 65 who is reemployed?':
   'under 65|reemployed|suspended',
 'A member who is 60 at retirement but lacks 120 contributions gets ___.':
   'lacks 120 contributions|lump sum|total contributions paid',
 'A retiree with no primary beneficiaries dies within 60 months of starting his pension. The secondary beneficiaries get ___.':
   "no primary beneficiaries|within 60 months|lump sum|rest of the 5-year guaranteed period|excluding dependents' pension",
 'Death benefit when the member paid at least 36 monthly contributions before the semester of death':
   'at least 36|Monthly pension|primary beneficiaries|secondary beneficiaries|lump sum|36 times',
 'A disabled member who got a lump sum and is reemployed not earlier than ___ from the disability becomes a new member.':
   'lump sum|reemployed|new member',
 'Disabilities deemed permanent TOTAL':
   'sight of both eyes|two limbs|ankle or wrists|complete paralysis|brain injury|imbecility or insanity|approved by the SSS',
 'Permanent partial disability (after 36 contributions): months of pension for loss of one hand / one arm / one foot / one leg':
   'one hand|one arm|one foot|one leg',
 'Permanent partial disability: months of pension for one thumb / one index finger / one big toe / sight of one eye':
   'one thumb|one index finger|one big toe|sight of one eye',
 'Permanent partial disability: months of pension for hearing of one ear / hearing of both ears / both ears':
   'hearing of one ear|hearing of both ears|both ears',
 'When is a permanent partial disability pension paid in a lump sum?':
   'lump sum|less than 12 months',
 'Funeral benefit under RA 11199':
   'funeral benefit|cash or in kind|IRR|variable',
 'Daily sickness benefit amount, and who pays it':
   'daily sickness benefit|who pays|average daily salary credit|employer|SSS',
 'Within how many days must the employee notify the employer of sickness?':
   'notify',
 'When does the sickness allowance begin to be paid?':
   'sickness allowance|begin|sick leaves with full pay|used up',
 'Examples of involuntary separation':
   'involuntary separation|labor-saving devices|redundancy|retrenchment|closure or cessation|disease or illness',
 'If two or more compensable contingencies occur at the same time, ___.':
   'two or more|same time|highest benefit',
 'Penalty for failing to register employees or to deduct and remit contributions':
   'failing to register|deduct and remit|Fine|imprisonment',
 'If an association, partnership or corporation violates RA 11199, who is liable?':
   'association, partnership or corporation|managing head|directors|partners',
 'Making false statements to obtain SSS benefits or loans is penalized under ___ of the Revised Penal Code.':
   'false statements|Article 172|falsification by private individual',
 'An SSS employee who misappropriates SSS funds suffers the penalties under ___ of the Revised Penal Code.':
   'misappropriates|Article 217|malversation',
 'How are doubts in interpreting the Labor Code and its rules resolved?':
   'doubts|interpreting',
 'Prohibition against elimination or diminution of benefits':
   'elimination or diminution|Nothing|eliminate or diminish|supplements|employee benefits|promulgated',
 'Labor standards':
   'minimum requirements|laws and rules|Wages|Hours of work|COLA|monetary and welfare benefits',
 'Are "wage", "salary", and "pay" different in meaning?':
   'wage|salary|pay|synonymous|reward or recompense',
 'The remuneration or earnings, however designated, capable of being expressed in terms of money, whether fixed or ascertained on a time, task, piece, or commission basis, or other method of calculating the same, payable by an employer to an employee under a written or unwritten contract of employment for work done or to be done, or for services rendered or to be rendered':
   'remuneration or earnings|expressed in terms of money|time, task, piece, or commission|employer to an employee|contract of employment',
 'Besides money, wage also includes ___.':
   'Besides money|fair and reasonable value|Secretary of Labor|board, lodging, or other facilities|customarily furnished|profit',
 'Basic pay (basic salary)':
   'basic pay|rate of pay|standard work period|excluding|bonuses|overtime',
 'Primary mode the State promotes for settling wages and other terms of employment':
   'primary mode|settling wages',
 'Who prescribes the regional minimum wage rates?':
   'regional minimum wage|Regional Tripartite Wages and Productivity Boards',
 'Can a wage order stop workers from bargaining for higher wages?':
   'wage order|bargaining',
 'Workers excepted from wage increases under wage orders':
   'excepted|wage orders|Barangay Micro Business Enterprises|Certificate of Authority',
 'Pay for work on a regular holiday (first 8 hours)':
   'regular holiday|first 8 hours',
 'Which establishments are exempt from HOLIDAY PAY because of size?':
   'size|Retail and service|fewer than 10 workers',
 'Employees excluded from holiday pay':
   'excluded|Government employees|retail and service|fewer than 10 workers|kasambahay|personal service|managerial employees|managerial staff|field personnel|unsupervised',
 'Three conditions for a managerial employee to be excluded':
   'three conditions|managerial employee|manage|directs the work|2 or more employees|hire or fire|particular weight',
 'Officers or members of the managerial staff may not spend more than ___ of their weekly hours on work not closely related to their managerial duties.':
   'managerial staff|weekly hours|not closely related',
 'An employee on leave WITHOUT pay the day before a regular holiday, who does not work on the holiday, gets ___.':
   'leave WITHOUT pay|day before|does not work',
 'The day before the holiday is a rest day or non-workday. When is the employee entitled to holiday pay?':
   'rest day or non-workday|worked|day immediately before',
 'Premium pay':
   'premium pay|Additional compensation|within 8 hours|rest days|special days',
 'Special (non-working) day, unworked':
   'unworked|No work, no pay|company policy|practice|CBA',
 'If employee worked on a special (non-working) day, the employee shall be paid an additional ___ of the basic wage on the first eight hours of work.':
   'special (non-working) day|first eight hours',
 'Worked on a special (non-working) day that is also the rest day':
   'also the rest day',
 'Worked on a regular holiday that is also the rest day':
   'also the rest day',
 'Employees excluded from PREMIUM PAY':
   'excluded|Government employees|kasambahay|personal service|managerial employees|managerial staff|paid by results|piece rate|field personnel',
 'Field personnel':
   'field personnel|regularly work away|principal or branch office|cannot be determined with reasonable certainty',
 'Weekly rest day':
   'weekly rest day|24 consecutive hours|6 consecutive normal work days',
 'Who schedules the weekly rest day, and whose preference must be respected?':
   'schedules|preference|employer|CBA|DOLE rules|religious grounds',
 'When may an employer require work on the scheduled rest day?':
   'require work|scheduled rest day|emergencies|machinery|abnormal pressure of work|perishable goods|continuous operations|analogous cases',
 'Normal hours of work':
   'normal hours',
 'Hours worked include ___.':
   'Hours worked|on duty|prescribed workplace|suffered or permitted to work',
 'Meal period the employer must give':
   'meal period|60 minutes|regular meals',
 'Can undertime on one day offset overtime on another day?':
   'undertime|offset overtime|leave on another day',
 'Overtime on an ordinary working day':
   'ordinary working day',
 'Overtime on a special day, rest day, or regular holiday':
   'special day, rest day, or regular holiday|ON THAT DAY',
 'When may an employer require compulsory overtime?':
   'compulsory overtime|War or declared emergency|loss of life or property|public safety|urgent work on machines|perishable goods|before the 8th hour|favorable weather',
 'Which establishments are exempt from NIGHT SHIFT DIFFERENTIAL because of size?':
   'size|Retail and service|fewer than FIVE (5) workers',
 'How do you get the hourly rate for OT and NSD?':
   'hourly rate|OT and NSD',
 '13th month pay amount':
   '13th month pay|1/12|total basic salary|calendar year',
 'Employers NOT covered by PD 851':
   'NOT covered|Government|GOCCs|already paying|household helpers|personal service|commission, boundary or task|fixed amount|piece-rate workers ARE covered',
 'Is a kasambahay entitled to 13th month pay?':
   'kasambahay|Batas Kasambahay',
 'Service incentive leave':
   'service incentive leave|5 days with pay|1 year of service',
 '"At least one year of service" means ___.':
   'At least one year of service|12 months|continuous or broken|authorized absences|paid regular holidays',
 'What happens to unused service incentive leave?':
   'unused|commuted to cash|end of the year|resignation or separation',
 'Employees excluded from service incentive leave':
   'excluded|Government employees|personal service|managerial|field personnel|already enjoying|5 days paid vacation leave|fewer than 10',
 'Are vacation and sick leaves mandated by law?':
   'mandated by law|5-day service incentive leave',
 'Maternity leave for miscarriage or emergency termination of pregnancy':
   'miscarriage|emergency termination',
 'Compulsory postnatal leave':
   'compulsory postnatal',
 'Emergency termination of pregnancy':
   'emergency termination of pregnancy|Pregnancy loss|20th week|stillbirth',
 "How many maternity leave days may the mother allocate to the child's father?":
   'allocate|father|7 days|whether or not they are married|on top of paternity leave',
 'Can maternity leave be allocated in case of miscarriage or emergency termination?':
   'allocated|miscarriage',
 'Conditions for paternity leave':
   'conditions|Employee at the time of delivery|cohabiting|reasonable time|given birth or miscarried',
 'Is unused paternity leave convertible to cash?':
   'convertible to cash',
 'Meaning of "cohabiting" for paternity leave':
   'cohabiting|live together|apart because of work',
 'Is unused solo parent leave convertible to cash?':
   'convertible to cash|agreed on it beforehand',
 'Conditions for parental leave of a solo parent':
   'conditions|6 months of service|notice to the employer|Solo Parent ID Card',
 "Who are solo parents? (sole care of the child due to the spouse's ___)":
   'sole care|Death|detention|incapacity|separation|nullity, annulment, or divorce|abandonment|born of rape',
 'Other solo parents under RA 11861':
   'OFW|12 uninterrupted months|unmarried mother or father|legal guardian, adoptive or foster parent|4th degree|pregnant woman',
 'Age limit for the child or dependent of a solo parent':
   'age limit|22 years|disability',
}

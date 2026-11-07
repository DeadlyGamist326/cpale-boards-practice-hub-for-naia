"""RFBT flashcards. Built from the laws themselves (statutes are public domain), not from review-center handouts.
Each card: (front, back, source)."""
import html, json

SSL = [
 ("The law now governing the Social Security System", "RA 11199, the Social Security Act of 2018 (amending RA 8282)", "RA 11199"),
 ("Compulsory SSS coverage applies to all employees not over ___ years of age and their employers.", "60", "RA 11199, Sec. 9"),
 ("Coverage of an employer takes effect on ___.", "The first day of its operation", "RA 11199, Sec. 10"),
 ("Coverage of an employee takes effect on ___.", "The first day of his or her employment", "RA 11199, Sec. 10"),
 ("Coverage of a self-employed person takes effect upon ___.", "His or her registration with the SSS", "RA 11199, Sec. 10"),
 ("Employment that is purely casual and not for the purpose of the employer's occupation or business is ___ from compulsory coverage.", "Excluded", "RA 11199, Sec. 8(j)"),
 ("Government employees are covered by ___, not the SSS.", "GSIS (Government Service Insurance System)", "RA 11199, Sec. 8(j)"),
 ("Services performed for a foreign government or an international organization are ___ from SSS coverage (unless covered by an agreement).", "Excluded", "RA 11199, Sec. 8(j)"),
 ("Household helpers (kasambahay) are compulsorily covered if they earn at least ___ a month.", "₱1,000", "RA 11199, Sec. 9"),
 ("Land-based overseas Filipino workers under RA 11199 are ___ covered.", "Compulsorily", "RA 11199, Sec. 9-B"),
 ("A spouse who devotes full time to managing the household and family affairs may be covered as a ___.", "Non-working spouse (voluntary member), with the consent of the working spouse who is an SSS member", "RA 11199, Sec. 9"),
 ("The non-working spouse's contribution is based on ___ of the working spouse's monthly salary credit.", "One-half (50%)", "RA 11199, Sec. 9"),
 ("SSS contribution rate starting January 2025", "15% of the monthly salary credit: 10% employer, 5% employee", "RA 11199 schedule; SSS 2025"),
 ("Monthly salary credit (MSC) range starting January 2025", "Minimum ₱5,000; maximum ₱35,000", "SSS 2025"),
 ("Penalty for late remittance of SSS contributions", "2% per month on the unpaid contributions, from the date they fell due until paid", "RA 11199, Sec. 22"),
 ("Prescriptive period for the SSS to collect unpaid contributions", "20 years from the time the delinquency is known or the assessment is made by the SSS", "RA 11199, Sec. 22(b)"),
 ("SSS benefits are exempt from ___.", "Tax, levy, garnishment, attachment, and other processes, except debts to the SSS", "RA 11199, Sec. 16"),
 ("Who are a member's dependents?", "(1) Legal spouse entitled to support; (2) unmarried, unemployed legitimate, legitimated, legally adopted or illegitimate child not over 21; (3) parent receiving regular support from the member", "RA 11199, Sec. 8(e)"),
 ("A child over 21 is still a dependent if ___.", "He or she is congenitally incapacitated, or became incapacitated while still a minor, and cannot support himself or herself", "RA 11199, Sec. 8(e)"),
 ("Primary beneficiaries", "The dependent spouse until he or she remarries, and the dependent legitimate, legitimated, legally adopted, and illegitimate children", "RA 11199, Sec. 8(k)"),
 ("Secondary beneficiaries", "The dependent parents; if none, any other person designated by the member", "RA 11199, Sec. 8(k)"),
 ("When illegitimate children concur with legitimate children, each illegitimate child gets ___ of a legitimate child's share.", "50%", "RA 11199, Sec. 8(k)"),
 ("Maximum number of dependent children counted for the dependents' pension", "Five (5), beginning with the youngest, without substitution", "RA 11199, Sec. 12-A"),
 ("Amount of the dependents' pension per dependent child", "10% of the monthly pension or ₱250, whichever is higher", "RA 11199, Sec. 12-A"),
 ("Optional retirement age", "60, if separated from employment and no longer self-employed", "RA 11199, Sec. 12-B"),
 ("Technical (mandatory) retirement age", "65, whether or not still working", "RA 11199, Sec. 12-B"),
 ("Minimum contributions for a MONTHLY retirement pension", "120 monthly contributions before the semester of retirement; if fewer, a lump sum equal to total contributions plus interest", "RA 11199, Sec. 12-B"),
 ("Minimum monthly pension", "₱1,200 with at least 10 credited years of service; ₱2,400 with at least 20", "RA 11199, Sec. 12"),
 ("Minimum contributions for the death benefit to be paid as a MONTHLY pension", "36 monthly contributions before the semester of death; if fewer, a lump sum", "RA 11199, Sec. 13"),
 ("Minimum contributions for a permanent total disability PENSION", "36 monthly contributions before the semester of disability", "RA 11199, Sec. 13-A"),
 ("Give the conditions deemed permanent total disability.", "Complete loss of sight of both eyes; loss of two limbs at or above the ankle or wrist; permanent complete paralysis of two limbs; brain injury causing incurable imbecility or insanity; and others set by the Commission", "RA 11199, Sec. 13-A"),
 ("Sickness benefit eligibility", "At least 3 monthly contributions in the 12 months before the semester of sickness, and confinement (hospital or home) for more than 3 days", "RA 11199, Sec. 14"),
 ("Daily sickness benefit amount", "90% of the member's average daily salary credit", "RA 11199, Sec. 14"),
 ("Maximum sickness benefit days in one calendar year", "120 days", "RA 11199, Sec. 14"),
 ("Who first pays the sickness benefit of an employed member?", "The employer advances it; the SSS later reimburses the employer", "RA 11199, Sec. 14"),
 ("An employee must notify the employer of sickness within ___.", "5 calendar days after the start of confinement", "RA 11199, Sec. 14"),
 ("Maternity benefit eligibility", "At least 3 monthly contributions in the 12 months before the semester of childbirth or miscarriage", "RA 11210; RA 11199, Sec. 14-A"),
 ("Maternity leave for live childbirth (normal or caesarean)", "105 days with full pay; +15 days if a solo parent; up to 7 days may be given to the child's father", "RA 11210"),
 ("Maternity leave for miscarriage or emergency termination of pregnancy", "60 days with full pay", "RA 11210"),
 ("Unemployment insurance (involuntary separation) benefit", "50% of the average monthly salary credit for up to 2 months; needs 36 monthly contributions, 12 of them in the 18 months before separation; member not over 60; once every 3 years", "RA 11199, Sec. 14-B"),
 ("Who decides disputes on SSS coverage, benefits, and contributions?", "The Social Security Commission; its decisions are appealable to the Court of Appeals", "RA 11199, Sec. 5"),
]

LABOR = [
 ("The remuneration or earnings, however designated, capable of being expressed in money, whether fixed or ascertained on a time, task, piece, or commission basis, payable by an employer to an employee under a written or unwritten contract of employment for work done or to be done.", "Wage", "Labor Code, Art. 97(f)"),
 ("If an employee works on a special (non-working) day, he or she is paid an additional ___ of the basic wage for the first eight hours.", "30%", "Labor Code; DOLE holiday pay rules"),
 ("Normal hours of work", "Not more than 8 hours a day", "Labor Code, Art. 83"),
 ("What counts as hours worked?", "(1) All time the employee must be on duty or at a prescribed workplace; (2) all time the employee is suffered or permitted to work", "Labor Code, Art. 84"),
 ("Meal period", "Not less than 60 minutes, not compensable. A shorter meal break (not less than 20 minutes) is compensable.", "Labor Code, Art. 85; IRR"),
 ("Night shift differential", "Not less than 10% of the regular wage for each hour worked between 10:00 PM and 6:00 AM", "Labor Code, Art. 86"),
 ("Overtime pay on an ordinary working day", "Additional at least 25% of the hourly rate (125%)", "Labor Code, Art. 87"),
 ("Overtime pay on a holiday or rest day", "Additional at least 30% of the hourly rate on that day", "Labor Code, Art. 87"),
 ("Can undertime on one day offset overtime on another day?", "No. Undertime work on any day cannot offset overtime work on another day.", "Labor Code, Art. 88"),
 ("When may an employer require emergency overtime work?", "War or national emergency; to prevent loss of life or property or imminent danger to public safety; urgent work on machines to avoid serious loss; to prevent loss of perishable goods; to finish work begun before the 8th hour when stopping would cause serious obstruction", "Labor Code, Art. 89"),
 ("Weekly rest period", "At least 24 consecutive hours after every 6 consecutive normal workdays", "Labor Code, Art. 91"),
 ("Pay for work on a scheduled rest day", "Additional at least 30% of the basic wage (130%)", "Labor Code, Art. 93"),
 ("Regular holiday, NOT worked", "100% of the daily wage", "Labor Code, Art. 94"),
 ("Regular holiday, worked (first 8 hours)", "200% of the daily wage", "Labor Code, Art. 94"),
 ("Regular holiday that falls on the rest day, worked", "200% + 30% of 200% = 260% of the daily wage", "DOLE holiday pay rules"),
 ("Special (non-working) day, NOT worked", "No pay (\"no work, no pay\"), unless a company policy or CBA grants it", "DOLE holiday pay rules"),
 ("Special (non-working) day that falls on the rest day, worked", "Additional 50% of the basic wage (150%)", "DOLE holiday pay rules"),
 ("How many regular holidays are there?", "12: New Year's Day, Maundy Thursday, Good Friday, Araw ng Kagitingan, Labor Day, Independence Day, National Heroes Day, Bonifacio Day, Christmas Day, Rizal Day, Eid'l Fitr, Eid'l Adha", "Labor Code, Art. 94; RA 9849"),
 ("Which establishments are exempt from paying holiday pay?", "Retail and service establishments regularly employing fewer than 10 workers", "Labor Code, Art. 94"),
 ("Employees NOT covered by the rules on hours of work, rest periods, and holidays", "Government employees; managerial employees; officers or members of the managerial staff; field personnel; family members dependent on the employer; domestic helpers; persons in the personal service of another; workers paid by results", "Labor Code, Art. 82"),
 ("Field personnel", "Non-agricultural employees who regularly work away from the principal place of business and whose actual hours of work in the field cannot be determined with reasonable certainty", "Labor Code, Art. 82"),
 ("Service incentive leave", "5 days with pay every year, for an employee who has rendered at least 1 year of service", "Labor Code, Art. 95"),
 ("Meaning of \"at least one year of service\" for service incentive leave", "Service within 12 months, whether continuous or broken, counted from the start of employment", "Labor Code IRR"),
 ("Who are NOT entitled to service incentive leave?", "Those already enjoying at least 5 days of paid vacation leave; employees of establishments regularly employing fewer than 10; plus those excluded under Art. 82", "Labor Code, Art. 95; IRR"),
 ("What happens to unused service incentive leave at year end?", "It is converted (commuted) to cash", "Labor Code IRR"),
 ("Law requiring 13th month pay", "PD 851", "PD 851"),
 ("Amount of 13th month pay", "At least 1/12 of the total basic salary earned within the calendar year", "PD 851"),
 ("Deadline for paying 13th month pay", "Not later than December 24 of every year", "PD 851 rules"),
 ("Who are entitled to 13th month pay?", "All rank-and-file employees, however paid, who worked at least 1 month during the calendar year", "PD 851 rules"),
 ("How often must wages be paid?", "At least once every 2 weeks, or twice a month at intervals not exceeding 16 days", "Labor Code, Art. 103"),
 ("Form of wage payment", "Legal tender. Not promissory notes, vouchers, coupons, tokens, tickets, chits, or any object other than legal tender.", "Labor Code, Art. 102"),
 ("Place of wage payment", "At or near the place of work (with limited exceptions)", "Labor Code, Art. 104"),
 ("Facilities vs. supplements", "Facilities (e.g., board and lodging) may be deducted from wages if customarily furnished, voluntarily accepted in writing, and charged at fair and reasonable value. Supplements are extra benefits and are not deductible.", "Labor Code, Art. 97(f); jurisprudence"),
 ("Who fixes the regional minimum wage rates?", "The Regional Tripartite Wages and Productivity Boards (RTWPBs), under the National Wages and Productivity Commission", "RA 6727"),
 ("Wage Rationalization Act", "RA 6727", "RA 6727"),
 ("Wage distortion", "A situation where a wage increase eliminates or severely contracts the intentional differences in wage rates between employee groups, based on skills, length of service, or other logical bases", "Labor Code, Art. 124"),
 ("How is wage distortion resolved in an ORGANIZED establishment?", "Through the grievance machinery under the CBA, and if unresolved, voluntary arbitration", "Labor Code, Art. 124"),
 ("How is wage distortion resolved in an UNORGANIZED establishment?", "Through the NCMB's conciliation; if unresolved, compulsory arbitration by the NLRC", "Labor Code, Art. 124"),
 ("Apprenticeship: maximum period and minimum wage", "Not more than 6 months; wage at least 75% of the applicable minimum wage", "Labor Code, Arts. 58–61"),
 ("Learnership: maximum period and minimum wage", "Not more than 3 months; wage at least 75% of the applicable minimum wage", "Labor Code, Arts. 73–75"),
 ("Night worker", "An employee who works at least 7 consecutive hours between 10:00 PM and 6:00 AM, including the interval from midnight to 5:00 AM", "RA 10151"),
 ("Paternity leave", "7 days with full pay, for the first 4 deliveries of the legitimate spouse with whom the employee is cohabiting", "RA 8187"),
 ("Solo parent leave", "7 working days with pay each year, after at least 6 months of service", "RA 8972, as amended by RA 11861"),
 ("Leave for women victims of violence (VAWC)", "Up to 10 days with pay", "RA 9262"),
 ("Special leave benefit for women", "Up to 2 months with full pay after surgery for gynecological disorders; needs at least 6 months of aggregate service in the last 12 months", "RA 9710 (Magna Carta of Women)"),
 ("Prescriptive period for money claims arising from employer-employee relations", "3 years from the time the cause of action accrued", "Labor Code, Art. 306 (formerly Art. 291)"),
 ("Kasambahay Law", "RA 10361 (Batas Kasambahay)", "RA 10361"),
 ("Rest periods of a kasambahay", "At least 8 hours of total daily rest, and at least 24 consecutive hours of weekly rest", "RA 10361"),
 ("Telecommuting Act", "RA 11165. Telecommuting employees get the same treatment and pay as comparable workers on the employer's premises.", "RA 11165"),
]

DECKS = [("ssl", "Social Security Law", "RA 11199: coverage, contributions, beneficiaries, benefits", SSL),
         ("labor", "Labor Standards", "Wages, hours of work, holidays, leaves, 13th month pay", LABOR)]

CSS = """
.fcv h2{margin-bottom:4px}
.fchint{color:var(--muted);margin:0 0 14px}
.card{display:flex;flex-direction:column;justify-content:center;gap:10px;width:100%;min-height:260px;border:2px solid var(--line);border-radius:16px;background:var(--soft);padding:22px 20px;text-align:center;font-family:Arial,Helvetica,sans-serif;font-size:19px;line-height:1.5;color:var(--ink)}
.card.flipped{background:var(--pink);border-color:var(--rose)}
.card .side{font-size:12px;font-weight:bold;text-transform:uppercase;letter-spacing:.1em;color:var(--muted)}
.card .fa{font-weight:bold;color:var(--deep);font-size:21px}
.card .src{font-size:13px;color:var(--muted)}
.fcbar{display:flex;gap:8px;justify-content:space-between;align-items:center;margin:14px 0}
.fcbar button{font-size:15px;font-weight:bold;background:var(--bg);color:var(--deep);border:1.5px solid var(--rose);border-radius:8px;padding:10px 14px}
.fcbar .flip{background:var(--rose);color:#ffffff;flex:1}
.fcmeta{display:flex;justify-content:space-between;align-items:center;color:var(--muted);font-size:14px;font-variant-numeric:tabular-nums}
.fcmeta button{background:none;border:0;color:var(--rose);font-weight:bold;font-size:14px;padding:4px 0}
.fclist{margin-top:22px}
.fclist summary{cursor:pointer;font-weight:bold;color:var(--deep)}
.fclist ol{padding-left:22px}
.fclist li{margin-bottom:10px}
.fclist .a{display:block;color:var(--deep);font-weight:bold}
@media (max-width:600px){.card{font-size:20px;min-height:300px}.card .fa{font-size:22px}.fcbar button{font-size:17px;padding:12px 14px}}
"""

JS = r"""
function initDeck(el){
  if(!el||el.dataset.ok)return;el.dataset.ok=1;
  const cards=JSON.parse(el.querySelector("script.deck").textContent),key="deck-"+el.id;
  let order=cards.map((_,i)=>i),i=0,back=false;
  try{const s=JSON.parse(localStorage.getItem(key)||"null");if(s&&s.order&&s.order.length===cards.length){order=s.order;i=s.i||0}}catch(e){}
  const card=el.querySelector(".card"),cnt=el.querySelector(".cnt");
  const esc=t=>t.replace(/&/g,"&amp;").replace(/</g,"&lt;");
  function draw(){const c=cards[order[i]];card.classList.toggle("flipped",back);
    card.innerHTML=back?'<span class="side">Answer</span><span class="fa">'+esc(c[1])+'</span><span class="src">'+esc(c[2])+'</span>'
                       :'<span class="side">Question</span><span>'+esc(c[0])+'</span><span class="src">Tap to show the answer</span>';
    cnt.textContent=(i+1)+" / "+cards.length;try{localStorage.setItem(key,JSON.stringify({order,i}))}catch(e){}}
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
        data = json.dumps([list(c) for c in cards], ensure_ascii=False).replace("</", "<\\/")
        lst = "".join(f'<li>{html.escape(f)}<span class="a">{html.escape(b)}</span></li>' for f, b, _ in cards)
        views.append(f'''<div class="fcv" id="fc-{slug}" hidden><div class="bar"><button type="button" class="back" data-home>← Home</button></div>
<p class="crumb">RFBT</p><h2>{title}</h2><p class="fchint">Tap the card to flip it. Use Next and Back to move through the deck.</p>
<button type="button" class="card" aria-live="polite"></button>
<div class="fcbar"><button type="button" class="prev">← Back</button><button type="button" class="flip">Flip</button><button type="button" class="next">Next →</button></div>
<div class="fcmeta"><span class="cnt"></span><span><button type="button" class="shuf">Shuffle</button> · <button type="button" class="rst">Start over</button></span></div>
<details class="fclist"><summary>See all {len(cards)} cards</summary><ol>{lst}</ol></details>
<script type="application/json" class="deck">{data}</script></div>''')
    return "".join(boxes), "".join(views)

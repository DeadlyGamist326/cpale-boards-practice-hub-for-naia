"""Make the RFBT handout crops pack (private; output is never committed).
Run in a folder holding the two handout PDFs named ssl.pdf and ls.pdf:  python3 crops_make.py
Writes crops2.json (rfbt-crops pack) and cr_*.jpg previews. Then encrypt with crops_encrypt.py."""
import re, sys, math, json, hashlib, base64, io, subprocess, collections, html
from PIL import Image
sys.path.insert(0, '/home/claude/cpale-boards-practice-hub-for-naia/tools')
import rfbt_flashcards as R
STOP = set("the a an of and or to in on for by is are be shall any his her their its with as at from that this which who whom not no if than per under".split())
def toks(t):
    t = html.unescape(t).lower().replace(",", "").replace("₱", " ")
    t = re.sub(r"\bp(?=\d)", " ", t); t = re.sub(r"(\d)\.00\b", r"\1", t)
    return set(w for w in re.findall(r"[a-z0-9]+", t) if w not in STOP and len(w) > 1)

FULL = {'ls.pdf': {8, 9, 10, 11}}
def lines_of(pdf):
    subprocess.run(['pdftotext', '-bbox-layout', pdf, 'bb.html'], check=True)
    s = open('bb.html', encoding='utf-8').read()
    out = []
    for pi, page in enumerate(re.findall(r'<page .*?</page>', s, re.S), 1):
        bp = re.search(r'>Page</word>\s*<word[^>]*>(\d+)</word>', page)
        for m in re.finditer(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</line>', page, re.S):
            x0, y0, x1, y1 = map(float, m.groups()[:4])
            words = [(float(a), float(b), float(c), float(d), html.unescape(t)) for a, b, c, d, t in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', m.group(5))]
            txt = " ".join(w[4] for w in words)
            if x0 < 30 or not txt.strip(): continue
            full = FULL.get(pdf, set())
            out.append(dict(p=pi, bp=int(bp.group(1)) if bp else None, col=0 if (x0 < 306 or pi in full) else 1, full=pi in full, x0=x0, y0=y0, x1=x1, y1=y1, t=txt, tk=toks(txt), words=words))
    out.sort(key=lambda l: (l['p'], l['col'], l['y0']))
    return out

def best_window(L, q, idf, skip):
    best = None
    for i in range(len(L)):
        if L[i]['p'] in skip: continue
        if L[i].get('full') and len(L[i]['t']) < 3: continue
        cov = set(); 
        for w in range(1, 15):
            j = i + w - 1
            if j >= len(L) or L[j]['p'] != L[i]['p'] or L[j]['col'] != L[i]['col']: break
            if w > 1 and L[j]['y0'] - L[j-1]['y1'] > 30: break
            cov |= (L[j]['tk'] & q)
            sc = sum(idf[t] for t in cov) / (1 + 0.035 * w) * (0.8 if L[i].get('full') else 1)
            if not best or sc > best[0]: best = (sc, i, j)
    return best

def extend_up(L, i):
    # include the bullet heading (➢) above, up to 6 lines
    k = i
    for _ in range(10):
        if L[k]['t'].lstrip().startswith('➢') or k == 0: break
        if L[k-1]['p'] != L[k]['p'] or L[k-1]['col'] != L[k]['col']: break
        k -= 1
    return k if L[k]['t'].lstrip().startswith('➢') else i

pages = {}
def page_img(pdf, p):
    key = (pdf, p)
    if key not in pages:
        subprocess.run(['pdftoppm', '-r', '144', '-gray', '-f', str(p), '-l', str(p), '-png', pdf, 'pg'], check=True)
        import glob
        f = sorted(glob.glob('pg-*.png'))[-1]
        pages[key] = Image.open(f).convert('L'); import os; os.remove(f)
    return pages[key]

from PIL import ImageDraw
def is_head(l):
    t = l['t'].strip()
    letters = re.sub(r'[^A-Za-z]', '', t)
    if l.get('full') or len(letters) < 4 or t.upper() != t or 'PAGE' in t or 'HANDOUT' in t: return False
    cl = 0 if l['col'] == 0 else 306
    cx = (l['x0'] + l['x1']) / 2 - cl
    return abs(cx - 162) < 45 and (l['x1'] - l['x0']) < 260 and not t.startswith(('➢', 'o ', '▪'))
def find_head(L, i):
    k = i - 1
    while k >= 0 and L[k]['p'] >= L[i]['p'] - 1 and i - k < 120:
        if is_head(L[k]) and not L[k].get('full'):
            ks = [k]
            while ks[0] - 1 >= 0 and is_head(L[ks[0] - 1]) and L[ks[0]]['y0'] - L[ks[0] - 1]['y1'] < 8 and L[ks[0]-1]['p'] == L[k]['p']: ks.insert(0, ks[0] - 1)
            while ks[-1] + 1 < len(L) and is_head(L[ks[-1] + 1]) and L[ks[-1] + 1]['y0'] - L[ks[-1]]['y1'] < 8 and L[ks[-1]+1]['p'] == L[k]['p']: ks.append(ks[-1] + 1)
            return ks
        k -= 1
    return None

import os
MAXL = 50          # max text lines in one crop
MAXH = 2600        # max crop height in px
HL = (170, 214, 255)   # light blue, applied with multiply (transparent)

def foot_cut(L):
    """(p,col) -> y where footnotes start."""
    cut = {}
    for k, l in enumerate(L):
        key = (l['p'], l['col'])
        if key in cut: continue
        cl = 30 if l['col'] == 0 or l.get('full') else 306
        prev = L[k-1] if k and (L[k-1]['p'], L[k-1]['col']) == key else None
        if l['y0'] > 500 and re.match(r'^\d{1,3}\s+\S', l['t'].strip()) and l['x0'] < cl + 22 and (prev is None or l['y0'] - prev['y1'] >= 10):
            cut[key] = l['y0'] - 1
    return cut

def body_line(l, cut):
    if l['y1'] - l['y0'] > 15: return False          # "Page N of 368"
    return l['y0'] < cut.get((l['p'], l['col']), 1e9)

def is_bullet(l, ch):
    t = l['t'].strip()
    return t == ch or t.startswith(ch + ' ')

def next_head(L, j, last_p):
    k = j + 1
    while k < len(L) and L[k]['p'] <= last_p:
        if is_head(L[k]): return k
        k += 1
    return k

def unit_for(L, i, j, cut):
    """Return (lines, header_indices_or_None) for the card whose best window is i..j."""
    ok = lambda k: body_line(L[k], cut)
    if L[i].get('full'):
        a = i
        while a > 0 and L[a-1]['p'] == L[i]['p'] and not re.match(r'^\d+\.$', L[a]['t'].strip()): a -= 1
        b = j
        while b + 1 < len(L) and L[b+1]['p'] == L[i]['p'] and not re.match(r'^\d+\.$', L[b+1]['t'].strip()): b += 1
        qk = a
        while qk > 0 and 'Q:' not in L[qk]['t'][:6]: qk -= 1
        u = [k for k in range(a, b + 1) if ok(k)]
        return u, ([qk] if qk not in u and 'Q:' in L[qk]['t'][:6] else None)
    hk = find_head(L, i)
    h0 = hk[-1] + 1 if hk else max(0, i - 40)
    nh = next_head(L, j, L[j]['p'] + 1)
    sec = [k for k in range(h0, nh) if ok(k) and not L[k].get('full')]
    if hk and len(sec) <= MAXL:
        return list(hk) + sec, None
    # the ➢ item that holds the window
    def item(ch, lo, hi):
        a = i
        while a > lo and not is_bullet(L[a], ch): a -= 1
        b = j + 1
        while b < hi and not is_bullet(L[b], ch) and not is_head(L[b]): b += 1
        return [k for k in range(a, b) if ok(k)]
    u = item('➢', h0, nh)
    if len(u) <= MAXL: return u, hk
    lo = u[0]; hi = u[-1] + 1
    u2 = item('o', lo, hi)
    if len(u2) <= MAXL: return u2, hk
    return [k for k in range(i, j + 1) if ok(k)], hk

def col_box(l):
    if l.get('full'): return 30, 606
    return (30, 306) if l['col'] == 0 else (306, 606)

def seg_crop(L, ks, hit_lines, q, idf):
    l0 = L[ks[0]]; img = page_img(CUR_PDF[0], l0['p']); sx = img.width / 612.0
    cl, cr = col_box(l0)
    left = max(cl, min(L[k]['x0'] for k in ks) - 6); right = min(cr, max(max(L[k]['x1'] for k in ks) + 6, cr - 10))
    import numpy as np
    a = np.asarray(img)
    X0, X1 = int(left * sx), int(right * sx)
    def blank(y): return y < 0 or y >= a.shape[0] or (a[y, X0:X1] < 150).sum() == 0
    def snap(y, step, lim):
        y = int(y * sx)
        for d in range(int(lim * sx)):
            if blank(y + step * d): return y + step * d
        return y
    top = snap(l0['y0'] - 1, -1, 8)
    bot = snap(max(L[k]['y1'] for k in ks) + 1, 1, 10)
    # never run into the next text line
    nxt = [l['y0'] for l in L if l['p'] == l0['p'] and col_box(l) == col_box(l0) and l['y0'] > max(L[k]['y1'] for k in ks) - 1 and l is not L[ks[-1]] and L.index(l) not in ks]
    if nxt: bot = min(bot, int((min(nxt) - 0.5) * sx))
    prv = [l['y1'] for l in L if l['p'] == l0['p'] and col_box(l) == col_box(l0) and l['y1'] < l0['y0'] + 1 and L.index(l) not in ks]
    if prv: top = max(top, int((max(prv) + 0.5) * sx))
    box = (X0, top, X1, bot)
    body = img.crop(box).convert('RGB')
    over = Image.new('RGB', body.size, (255, 255, 255)); dr = ImageDraw.Draw(over)
    for k in ks:
        if k not in hit_lines: continue
        ws = L[k]['words']; hit = [bool(toks(w[4]) & q) and any(idf[t] > 1.0 for t in toks(w[4]) & q) for w in ws]
        for n in range(len(ws)):
            if not hit[n] and any(hit[max(0, n - 2):n]) and any(hit[n + 1:n + 3]): hit[n] = True
        runs = []; st = None
        for n, h in enumerate(hit + [False]):
            if h and st is None: st = n
            if not h and st is not None: runs.append((st, n - 1)); st = None
        for s_, e_ in runs:
            if e_ == s_:
                wt = toks(ws[s_][4]) & q
                if not any(t.isdigit() for t in wt) and not (max((idf[t] for t in wt), default=0) > 3.2 and len(re.sub(r'\W', '', ws[s_][4])) >= 6): continue
            X0 = ws[s_][0] - 1.5; X1 = ws[e_][2] + 1.5; Y0 = ws[s_][1] - 1; Y1 = ws[s_][3] + 1
            dr.rectangle([X0 * sx - box[0], Y0 * sx - box[1], X1 * sx - box[0], Y1 * sx - box[1]], fill=HL)
    return ImageChops.multiply(body, over)

from PIL import ImageChops
def stack(parts):
    W = max(p.width for p in parts); gap = 26
    H = sum(p.height for p in parts) + gap * (len(parts) - 1)
    out = Image.new('RGB', (W, H), 'white'); y = 0; d = ImageDraw.Draw(out)
    for n, p in enumerate(parts):
        if n:
            yy = y - gap // 2
            for xx in range(20, W - 20, 14): d.line([(xx, yy), (xx + 6, yy)], fill=(200, 160, 175), width=2)
        out.paste(p, (0, y)); y += p.height + gap
    return out

def build(L, unit, hk, i, j, q, idf):
    hit_lines = set(range(i, j + 1))
    segs = []
    for k in unit:
        if segs and (L[segs[-1][-1]]['p'], L[segs[-1][-1]]['col']) == (L[k]['p'], L[k]['col']): segs[-1].append(k)
        else: segs.append([k])
    parts = []
    if hk and hk[0] not in unit:
        parts.append(seg_crop(L, list(hk), set(), q, idf))
    parts += [seg_crop(L, s, hit_lines, q, idf) for s in segs]
    return stack(parts)

def card_key(front): return hashlib.sha1(front.encode('utf-8')).hexdigest()[:12]
CUR_PDF = [None]
pack = {}; report = []
for f_ in __import__('glob').glob('cr_*.jpg'): os.remove(f_)
for name, title, pdf, cards, skip in (("ssl", "Social Security Law handout", "ssl.pdf", R.SSL, {1, 2, 11, 12}), ("labor", "Labor Standards handout", "ls.pdf", R.LABOR, {12, 13})):
    L = lines_of(pdf); CUR_PDF[0] = pdf; cut = foot_cut(L)
    df = collections.Counter(); [df.update(l['tk']) for l in L]
    N = len(L); idf = collections.defaultdict(lambda: 0, {t: math.log(N / (1 + c)) for t, c in df.items()})
    for f, a, src in cards:
        q = toks(f + " " + a)
        sk = set() if f.startswith("Deadline for paying the 13th") else skip
        sc, i, j = best_window(L, q, idf, sk)
        unit, hk = unit_for(L, i, j, cut)
        if i not in unit: unit = sorted(set(unit) | {k for k in range(i, j + 1) if body_line(L[k], cut)})
        if not unit:
            print('EMPTY', name, f[:50], L[i]['p'], L[i]['t'][:50]); unit = list(range(i, j + 1))
        crop = build(L, unit, hk, i, j, toks(a), idf)
        if crop.height > MAXH:
            unit = [k for k in range(extend_up(L, i), j + 1) if body_line(L[k], cut)]
            crop = build(L, unit, hk or find_head(L, i), i, j, toks(a), idf)
        buf = io.BytesIO(); crop.save(buf, 'JPEG', quality=62, optimize=True)
        p0 = L[unit[0]]
        ref = f"{title}, p. {p0['bp']}" if p0['bp'] else f"{title}, PDF page {p0['p']}"
        pack[name + ":" + card_key(f)] = {"ref": ref, "img": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()}
        report.append((name, len(report), crop.size, len(unit), f[:55]))
        crop.save(f'cr_{name}_{len(report):03d}.jpg')
json.dump({"kind": "rfbt-crops", "v": 2, "crops": pack}, open('crops2.json', 'w'))
for r in report: print(*r, sep=" | ")
print('size MB', os.path.getsize('crops2.json') / 1e6)

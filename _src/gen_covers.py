"""Generates ten original abstract SVG covers in the Verita palette.
Each cover is tied to its post's topic. No text inside the SVGs (titles are HTML overlays)."""
import math, random, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'blog', 'covers')
os.makedirs(OUT, exist_ok=True)
W, H = 1200, 750
CREAM = '#e6e2d8'

def head(uid):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-hidden="true">
<defs>
<radialGradient id="{uid}bg" cx="62%" cy="42%" r="85%"><stop offset="0" stop-color="#1b1f2b"/><stop offset=".55" stop-color="#11141c"/><stop offset="1" stop-color="#0a0c11"/></radialGradient>
<linearGradient id="{uid}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f0d79a"/><stop offset=".5" stop-color="#c79a45"/><stop offset="1" stop-color="#8a6526"/></linearGradient>
<linearGradient id="{uid}gv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f0d79a" stop-opacity=".9"/><stop offset="1" stop-color="#8a6526" stop-opacity="0"/></linearGradient>
<pattern id="{uid}grid" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60 0H0V60" fill="none" stroke="{CREAM}" stroke-opacity=".05" stroke-width="1"/></pattern>
</defs>
<rect width="{W}" height="{H}" fill="url(#{uid}bg)"/>
<rect width="{W}" height="{H}" fill="url(#{uid}grid)"/>
'''

def save(name, uid, body):
    with open(os.path.join(OUT, name + '.svg'), 'w') as f:
        f.write(head(uid) + body + '</svg>\n')

def poly(pts):
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)

# 1. retention leak: a vessel of dots, the ones near a gap drift away
def c1():
    u = 'a'; r = random.Random(1); cx, cy, R = 700, 380, 230
    s = f'<circle cx="{cx}" cy="{cy}" r="{R+34}" fill="none" stroke="{CREAM}" stroke-opacity=".12"/>'
    gap0, gap1 = math.radians(20), math.radians(70)
    arc = []
    a = gap1
    while a < gap0 + 2 * math.pi:
        arc.append((cx + (R + 34) * math.cos(a), cy + (R + 34) * math.sin(a))); a += .03
    s += f'<path d="{poly(arc)}" fill="none" stroke="url(#{u}g)" stroke-width="3" stroke-linecap="round"/>'
    step = 26
    for row in range(-9, 10):
        for col in range(-9, 10):
            x = cx + col * step + (row % 2) * step / 2; y = cy + row * step * .87
            d = math.hypot(x - cx, y - cy)
            if d > R: continue
            ang = math.atan2(y - cy, x - cx) % (2 * math.pi)
            inside = gap0 <= ang <= gap1 and d > R * .45
            if inside:
                k = (d - R * .45) / (R * .55)
                dx = (x - cx) / max(d, 1) * k * 190 + r.uniform(-8, 8); dy = (y - cy) / max(d, 1) * k * 190 + r.uniform(-8, 8)
                s += f'<circle cx="{x+dx:.1f}" cy="{y+dy:.1f}" r="{max(1.2,5-k*3.2):.1f}" fill="#f0d79a" opacity="{max(.06,.75-k*.7):.2f}"/>'
            else:
                s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.6" fill="url(#{u}g)" opacity="{.85 if d<R*.8 else .55:.2f}"/>'
    save('retention-budgets-leak', u, s)

# 2. bonus economics: value curve vs cost curve, hatched where cost overtakes
def c2():
    u = 'b'
    x0, x1, yb = 150, 1080, 600
    def val(t): return yb - 40 - 330 * (1 - math.exp(-2.6 * t))
    def cost(t): return yb - 20 - 30 * t - 500 * t ** 1.5
    ts = [i / 120 for i in range(121)]
    vp = [(x0 + t * (x1 - x0), val(t)) for t in ts]
    cp = [(x0 + t * (x1 - x0), cost(t)) for t in ts]
    cross = next(t for t in ts if cost(t) < val(t))
    s = f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{CREAM}" stroke-opacity=".3"/><line x1="{x0}" y1="{yb}" x2="{x0}" y2="120" stroke="{CREAM}" stroke-opacity=".3"/>'
    for i in range(1, 10):
        x = x0 + i * (x1 - x0) / 10
        s += f'<line x1="{x:.0f}" y1="{yb}" x2="{x:.0f}" y2="{yb+8}" stroke="{CREAM}" stroke-opacity=".3"/>'
    area = [(x0, yb)] + vp + [(x1, yb)]
    s += f'<path d="{poly(area)} Z" fill="url(#{u}gv)" opacity=".28"/>'
    s += f'<defs><pattern id="{u}h" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="9" stroke="{CREAM}" stroke-opacity=".35" stroke-width="2"/></pattern></defs>'
    seg = [p for p, t in zip(cp, ts) if t >= cross]
    segv = [p for p, t in zip(vp, ts) if t >= cross]
    s += f'<path d="{poly(seg)} L{poly(segv[::-1])[1:]} Z" fill="url(#{u}h)"/>'
    s += f'<path d="{poly(vp)}" fill="none" stroke="url(#{u}g)" stroke-width="5" stroke-linecap="round"/>'
    s += f'<path d="{poly(cp)}" fill="none" stroke="{CREAM}" stroke-opacity=".75" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/>'
    cxp = x0 + cross * (x1 - x0); cyp = val(cross)
    s += f'<line x1="{cxp:.0f}" y1="{cyp:.0f}" x2="{cxp:.0f}" y2="{yb}" stroke="#f0d79a" stroke-opacity=".5" stroke-dasharray="4 6"/>'
    s += f'<circle cx="{cxp:.0f}" cy="{cyp:.0f}" r="14" fill="none" stroke="#f0d79a" stroke-opacity=".5"/><circle cx="{cxp:.0f}" cy="{cyp:.0f}" r="7" fill="url(#{u}g)"/>'
    save('bonus-economics', u, s)

# 3. cashier funnel: narrowing tiers, leakage at one tier
def c3():
    u = 'c'; r = random.Random(3); cx = 640
    tiers = [(700, 'a'), (610, 'a'), (520, 'a'), (420, 'a'), (330, 'x'), (250, 'a')]
    y = 110; h = 78; gap = 16; s = ''
    for i, (w, k) in enumerate(tiers):
        nw = tiers[i + 1][0] if i + 1 < len(tiers) else w * .78
        pts = [(cx - w / 2, y), (cx + w / 2, y), (cx + nw / 2 - 12, y + h), (cx - nw / 2 + 12, y + h)]
        last = i == len(tiers) - 1
        fill = f'url(#{u}g)' if last else 'none'
        s += f'<path d="{poly(pts)} Z" fill="{fill}" fill-opacity="{.9 if last else 0}" stroke="{"#f0d79a" if last else CREAM}" stroke-opacity="{1 if last else .3+.06*i:.2f}" stroke-width="{2.2 if last else 1.6}"/>'
        if k == 'x':
            for j in range(16):
                px = cx + w / 2 - 6 + r.uniform(0, 140); py = y + h * .3 + r.uniform(0, 90) + j * 6
                s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r.uniform(2,5):.1f}" fill="#f0d79a" opacity="{r.uniform(.15,.7):.2f}"/>'
        y += h + gap
    for j in range(26):
        s += f'<circle cx="{cx+r.uniform(-60,60):.0f}" cy="{r.uniform(60,640):.0f}" r="{r.uniform(1.5,3.5):.1f}" fill="#f0d79a" opacity="{r.uniform(.2,.6):.2f}"/>'
    save('cashier-conversion-funnel', u, s)

# 4. KYC gates: nested arches with one narrow gate and a path through them
def c4():
    u = 'd'; cx, base = 600, 690; s = ''
    def arch(w, h, op, sw=1.6, col=CREAM):
        r = w / 2
        return f'<path d="M{cx-r} {base} V{base-h+r} A{r} {r} 0 0 1 {cx+r} {base-h+r} V{base}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{sw}"/>'
    sizes = [(880, 640), (720, 560), (580, 490), (460, 430), (350, 380), (260, 335), (190, 300)]
    for i, (w, h) in enumerate(sizes):
        base_i = base - i * 8
        r = w / 2
        col = '#f0d79a' if i == 4 else CREAM
        op = .9 if i == 4 else .16 + .07 * i
        s += f'<path d="M{cx-r} {base_i} V{base_i-h+r} A{r} {r} 0 0 1 {cx+r} {base_i-h+r} V{base_i}" fill="none" stroke="{col}" stroke-opacity="{op:.2f}" stroke-width="{3 if i==4 else 1.6}"/>'
    pts = []
    for i in range(46):
        t = i / 45; y = 720 - t * 520; x = cx + math.sin(t * 5) * (1 - t) * 90
        pts.append((x, y))
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{5-3.2*t:.1f}" fill="url(#{u}g)" opacity="{1-.5*t:.2f}"/>'
    s += f'<line x1="{cx-160}" y1="{base-4*8-4}" x2="{cx+160}" y2="{base-4*8-4}" stroke="#f0d79a" stroke-opacity=".5" stroke-dasharray="3 8"/>'
    save('kyc-onboarding-friction', u, s)

# 5. responsible gambling: protective domes over an activity wave with a threshold
def c5():
    u = 'e'; cx, cy = 600, 560; s = ''
    for i, R in enumerate([330, 275, 220]):
        a0, a1 = math.pi * 1.04, math.pi * 1.96
        x0, y0 = cx + R * math.cos(a0), cy + R * math.sin(a0); x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
        s += f'<path d="M{x0:.1f} {y0:.1f} A{R} {R} 0 0 1 {x1:.1f} {y1:.1f}" fill="none" stroke="url(#{u}g)" stroke-opacity="{.95-.25*i:.2f}" stroke-width="{4-i}" stroke-linecap="round"/>'
    ty = 470
    s += f'<line x1="170" y1="{ty}" x2="1030" y2="{ty}" stroke="#f0d79a" stroke-opacity=".6" stroke-dasharray="5 9"/>'
    wave = []
    for i in range(241):
        t = i / 240; x = 150 + t * 900
        y = 600 - (30 + 120 * t ** 1.6) * (.55 + .45 * math.sin(t * 38)) - 40 * t ** 3
        wave.append((x, y))
    s += f'<path d="{poly([(150,660)]+wave+[(1050,660)])} Z" fill="url(#{u}gv)" opacity=".18"/>'
    s += f'<path d="{poly(wave)}" fill="none" stroke="{CREAM}" stroke-opacity=".8" stroke-width="2.4" stroke-linejoin="round"/>'
    for (x, y), (x2, y2) in zip(wave, wave[1:]):
        if (y - ty) * (y2 - ty) < 0:
            s += f'<line x1="{x:.0f}" y1="{ty-70}" x2="{x:.0f}" y2="{ty+70}" stroke="#f0d79a" stroke-opacity=".35"/><circle cx="{x:.0f}" cy="{ty}" r="9" fill="url(#{u}g)"/><circle cx="{x:.0f}" cy="{ty}" r="18" fill="none" stroke="#f0d79a" stroke-opacity=".4"/>'
    save('responsible-gambling-product', u, s)

# 6. new market: contour terrain with a path of stepping stones and milestone flags
def c6():
    u = 'f'; s = ''
    for k in range(15):
        pts = []
        for i in range(181):
            a = i / 180 * 2 * math.pi
            rr = 40 + k * 26 + 14 * math.sin(3 * a + k * .35) + 9 * math.sin(5 * a - k * .2)
            pts.append((760 + rr * 1.55 * math.cos(a) + k * 6, 350 + rr * .9 * math.sin(a)))
        s += f'<path d="{poly(pts)} Z" fill="none" stroke="{CREAM}" stroke-opacity="{.07+.012*(14-k):.3f}" stroke-width="1.4"/>'
    path = [(110, 640), (250, 585), (390, 560), (500, 480), (620, 455), (730, 380), (850, 330), (960, 250), (1080, 175)]
    s += f'<path d="{poly(path)}" fill="none" stroke="#f0d79a" stroke-opacity=".28" stroke-width="2" stroke-dasharray="3 10"/>'
    for i, (x, y) in enumerate(path):
        r_ = 5 + i * .9
        s += f'<circle cx="{x}" cy="{y}" r="{r_:.1f}" fill="url(#{u}g)"/>'
        if i in (2, 5, 8):
            s += f'<line x1="{x}" y1="{y-r_}" x2="{x}" y2="{y-r_-52}" stroke="#f0d79a" stroke-width="2"/><path d="M{x} {y-r_-52} l30 11 l-30 11 Z" fill="url(#{u}g)"/>'
    save('new-regulated-market-timeline', u, s)

# 7. migration: dots handed from a fading cluster to a solid cluster across arcs
def c7():
    u = 'g'; r = random.Random(7); s = ''
    L = [(210 + (i % 6) * 38, 230 + (i // 6) * 40) for i in range(48)]
    Rr = [(800 + (i % 6) * 38, 230 + (i // 6) * 40) for i in range(48)]
    for i, (x, y) in enumerate(L):
        moved = i % 3 != 0
        s += f'<circle cx="{x}" cy="{y}" r="6" fill="{CREAM}" opacity="{.12 if moved else .6}"/>'
    for i, (x, y) in enumerate(Rr):
        s += f'<circle cx="{x}" cy="{y}" r="6" fill="url(#{u}g)" opacity="{.95 if i%3!=0 else .15}"/>'
    for i, ((x, y), (x2, y2)) in enumerate(zip(L, Rr)):
        if i % 3 == 0: continue
        mx = (x + x2) / 2; my = min(y, y2) - 90 - (i % 7) * 18
        s += f'<path d="M{x} {y} Q{mx} {my} {x2} {y2}" fill="none" stroke="url(#{u}g)" stroke-opacity="{.22+.05*(i%5):.2f}" stroke-width="1.4"/>'
    for i in range(14):
        t = r.uniform(.15, .85); i2 = r.randrange(48); (x, y), (x2, y2) = L[i2], Rr[i2]
        mx = (x + x2) / 2; my = min(y, y2) - 90 - (i2 % 7) * 18
        px = (1 - t) ** 2 * x + 2 * t * (1 - t) * mx + t * t * x2; py = (1 - t) ** 2 * y + 2 * t * (1 - t) * my + t * t * y2
        s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="4" fill="#f0d79a"/>'
    s += f'<rect x="170" y="560" width="860" height="2" fill="url(#{u}g)" opacity=".5"/>'
    save('platform-migration', u, s)

# 8. tracking: three ledgers of bars that almost agree, mismatches in gold
def c8():
    u = 'h'; r = random.Random(8); s = ''
    n = 44; base = [r.uniform(40, 120) for _ in range(n)]
    for row, y0 in enumerate([210, 400, 590]):
        s += f'<line x1="130" y1="{y0}" x2="1070" y2="{y0}" stroke="{CREAM}" stroke-opacity=".3"/>'
        for i in range(n):
            x = 150 + i * 20.5; h = base[i]; bad = False
            if row > 0 and r.random() < (.16 if row == 1 else .22):
                h = h * r.choice([.55, 1.35, .7]); bad = True
            if row > 0 and r.random() < .1: x += 7
            fill = '#f0d79a' if bad else CREAM
            s += f'<rect x="{x:.1f}" y="{y0-h:.1f}" width="9" height="{h:.1f}" fill="{fill}" opacity="{.95 if bad else .55}"/>'
    for i in range(n):
        s += f'<line x1="{150+i*20.5+4.5:.1f}" y1="215" x2="{150+i*20.5+4.5:.1f}" y2="590" stroke="{CREAM}" stroke-opacity=".05"/>'
    save('tracking-you-can-trust', u, s)

# 9. fractional vs full time: a complete ring beside a partly filled ring
def c9():
    u = 'i'; s = ''
    def ring(cx, cy, R, frac, gold):
        t = ''
        for i in range(60):
            a = i / 60 * 2 * math.pi - math.pi / 2
            x1, y1 = cx + (R + 14) * math.cos(a), cy + (R + 14) * math.sin(a)
            x2, y2 = cx + (R + (30 if i % 5 == 0 else 22)) * math.cos(a), cy + (R + (30 if i % 5 == 0 else 22)) * math.sin(a)
            t += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{CREAM}" stroke-opacity=".3"/>'
        t += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{CREAM}" stroke-opacity=".18" stroke-width="14"/>'
        a0 = -math.pi / 2; a1 = a0 + frac * 2 * math.pi
        if frac >= .999:
            t += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{CREAM}" stroke-opacity=".7" stroke-width="14"/>'
        else:
            x0, y0 = cx + R * math.cos(a0), cy + R * math.sin(a0); x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
            t += f'<path d="M{x0:.1f} {y0:.1f} A{R} {R} 0 {1 if frac>.5 else 0} 1 {x1:.1f} {y1:.1f}" fill="none" stroke="url(#{u}g)" stroke-width="14" stroke-linecap="round"/>'
            t += f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="13" fill="#f0d79a"/>'
        t += f'<circle cx="{cx}" cy="{cy}" r="{R-34}" fill="none" stroke="{CREAM}" stroke-opacity=".1"/>'
        return t
    s += ring(420, 375, 170, 1, False) + ring(800, 375, 170, .4, True)
    s += f'<line x1="600" y1="150" x2="600" y2="600" stroke="{CREAM}" stroke-opacity=".12" stroke-dasharray="3 9"/>'
    save('fractional-vs-full-time-leadership', u, s)

# 10. roadmap gap: stairs up on the left, a broken bridge to a platform on the right
def c10():
    u = 'j'; s = ''
    for i in range(7):
        x = 90 + i * 85; y = 640 - i * 62
        s += f'<rect x="{x}" y="{y}" width="85" height="{700-y}" fill="none" stroke="{CREAM}" stroke-opacity="{.25+.05*i:.2f}" stroke-width="1.6"/>'
    top = 640 - 6 * 62
    for i in range(4):
        x = 790 + i * 85; y = 500 - i * 22
        s += f'<rect x="{x}" y="{y}" width="85" height="{700-y}" fill="none" stroke="{CREAM}" stroke-opacity=".28" stroke-width="1.6"/>'
    s += f'<path d="M95 640 L180 640 L180 578 L265 578 L265 516 L350 516 L350 454 L435 454 L435 392 L520 392 L520 330 L605 {top}" fill="none" stroke="url(#{u}g)" stroke-width="4" stroke-linejoin="round"/>'
    s += f'<path d="M605 {top} L700 {top} L795 {top+40} L880 {top+70}" fill="none" stroke="#f0d79a" stroke-opacity=".6" stroke-width="3" stroke-dasharray="2 12" stroke-linecap="round"/>'
    for x, y in [(605, top), (700, top), (795, top + 40)]:
        s += f'<circle cx="{x}" cy="{y}" r="7" fill="url(#{u}g)"/>'
    s += f'<path d="M640 {top} V700" stroke="{CREAM}" stroke-opacity=".12" stroke-dasharray="3 9"/><path d="M780 {top+30} V700" stroke="{CREAM}" stroke-opacity=".12" stroke-dasharray="3 9"/>'
    save('roadmaps-stall', u, s)

for f in (c1, c2, c3, c4, c5, c6, c7, c8, c9, c10):
    f()
print('ok')

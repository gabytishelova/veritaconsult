#!/usr/bin/env python3
"""Builds the Verita blog: post pages, homepage data/patch for the minified bundle, CSS, sitemap, OG images.
Idempotent: safe to run repeatedly. Run from anywhere: python3 _src/build.py"""
import glob, html, json, math, os, re, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, '_src')
SITE = 'https://www.verita-consult.com'
BUNDLE = os.path.join(ROOT, 'assets', 'index-DJU1rbE0.js')
CSSF = os.path.join(ROOT, 'assets', 'index-Bie2yWpX.css')
CAL = 'https://calendly.com/verita-consult'

# ---------------------------------------------------------------- posts
def parse(path):
    raw = open(path, encoding='utf-8').read()
    head, body = raw.split('\n\n', 1)
    meta = dict(l.split(': ', 1) for l in head.strip().splitlines())
    words = len(re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', body).split())
    d = datetime.date.fromisoformat(meta['date'])
    meta.update(body=body.strip(), words=words, read=max(1, math.ceil(words / 200)),
                dt=d, long=f"{d.day} {d.strftime('%B %Y')}", short=f"{d.day} {d.strftime('%b %Y')}")
    return meta

posts = sorted((parse(p) for p in glob.glob(os.path.join(SRC, 'posts', '*.md'))), key=lambda p: p['dt'], reverse=True)

def inline(s):
    s = html.escape(s, quote=False)
    return re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" rel="noopener" target="_blank">\1</a>', s)

def render(body):
    out = []
    for block in re.split(r'\n\s*\n', body):
        lines = block.strip().splitlines()
        if not lines: continue
        if lines[0].startswith('## '):
            out.append(f'<h2>{inline(lines[0][3:])}</h2>')
        elif all(l.startswith('- ') for l in lines):
            out.append('<ul>' + ''.join(f'<li>{inline(l[2:])}</li>' for l in lines) + '</ul>')
        elif all(re.match(r'\d+\. ', l) for l in lines):
            out.append('<ol>' + ''.join(f"<li>{inline(re.sub(r'^\d+\. ', '', l))}</li>" for l in lines) + '</ol>')
        else:
            out.append(f"<p>{inline(' '.join(lines))}</p>")
    return '\n'.join(out)

# ---------------------------------------------------------------- shared chrome (copied from the live DOM)
LOGO_NAV = open(os.path.join(SRC, 'logo_nav.html')).read()
LOGO_FOOT = open(os.path.join(SRC, 'logo_footer.html')).read()
NAVLINK = 'font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted-foreground);text-decoration:none;font-weight:500;transition:color .2s'
LINKS = [('What We Do', '/#what-we-do'), ('How We Work', '/#how-we-work'), ('Who We Serve', '/#who-we-serve'), ('Blog', '/#blog')]

def nav_html():
    desk = ''.join(f'<a class="vp-navlink" href="{h}" style="{NAVLINK}">{t}</a>' for t, h in LINKS)
    mob = ''.join(f'<a href="{h}" style="display:block;padding:12px 0;font-size:14px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted-foreground);text-decoration:none;border-bottom:1px solid var(--border)">{t}</a>' for t, h in LINKS)
    return f'''<nav style="position:fixed;top:0;left:0;right:0;z-index:50;border-bottom:1px solid var(--border);background-color:rgba(12,14,20,.94);backdrop-filter:blur(12px)">
<div style="max-width:1200px;margin:0 auto;padding:0 32px;display:flex;align-items:center;justify-content:space-between;height:68px">
<a href="/" aria-label="Verita home" style="text-decoration:none;display:block">{LOGO_NAV}</a>
<div class="hide-mobile" style="display:flex;align-items:center;gap:40px">{desk}<a href="/#contact" style="font-size:12px;letter-spacing:.08em;text-transform:uppercase;font-weight:600;color:var(--primary-foreground);background-color:var(--accent);padding:9px 20px;text-decoration:none">Talk to us</a></div>
<button id="vp-menu-btn" class="show-mobile" aria-label="Menu" aria-expanded="false" aria-controls="vp-menu" style="background:none;border:none;color:var(--foreground);cursor:pointer;padding:4px"><svg width="22" height="16" viewBox="0 0 22 16" fill="none"><line x1="0" y1="1" x2="22" y2="1" stroke="currentColor" stroke-width="1.5"/><line x1="0" y1="8" x2="22" y2="8" stroke="currentColor" stroke-width="1.5"/><line x1="0" y1="15" x2="22" y2="15" stroke="currentColor" stroke-width="1.5"/></svg></button>
</div>
<div id="vp-menu" hidden style="border-top:1px solid var(--border);background-color:var(--background);padding:20px 32px 28px">{mob}<a href="/#contact" style="display:inline-block;margin-top:20px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;font-weight:600;color:var(--primary-foreground);background-color:var(--accent);padding:10px 22px;text-decoration:none">Talk to us</a></div>
</nav>'''

FLINK = 'font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted-foreground);text-decoration:none'
FOOT_LINKS = LINKS + [('Contact', '/#contact')]

def footer_html():
    fl = ''.join(f'<a href="{h}" style="{FLINK}">{t}</a>' for t, h in FOOT_LINKS)
    return f'''<footer style="border-top:1px solid var(--border);padding:36px 32px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;max-width:1200px;margin:0 auto">
<a href="/" aria-label="Verita home" style="text-decoration:none;display:block">{LOGO_FOOT}</a>
<nav aria-label="Footer" style="display:flex;flex-wrap:wrap;gap:8px 24px">{fl}</nav>
<p style="font-size:12px;color:var(--muted-foreground)">&copy; 2026 Verita IGAMING CONSULTANCY - UAE &middot; LATAM &middot; CYPRUS</p>
</footer>'''

PAGE_CSS = '''@media (max-width:860px){.hide-mobile{display:none!important}.show-mobile{display:block!important}}
@media (min-width:861px){.show-mobile{display:none!important}}
.vp-navlink:hover{color:var(--foreground)!important}'''

def page(p, older, newer):
    url = f"{SITE}/blog/{p['slug']}/"
    img = f"{SITE}/blog/covers/{p['slug']}.png"
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": p['title'], "description": p['desc'],
                     "datePublished": p['date'], "image": img, "mainEntityOfPage": url,
                     "author": {"@type": "Organization", "name": "Verita IGAMING CONSULTANCY"},
                     "publisher": {"@type": "Organization", "name": "Verita IGAMING CONSULTANCY"}})
    def pn(label, q):
        if not q: return '<span></span>'
        return f'<a class="vp-pn" href="/blog/{q["slug"]}/"><span class="vp-pn-l">{label}</span><span class="vp-pn-t font-display">{html.escape(q["title"])}</span></a>'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(p['title'])} | Verita IGAMING CONSULTANCY</title>
<meta name="description" content="{html.escape(p['desc'], quote=True)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(p['title'], quote=True)}">
<meta property="og:description" content="{html.escape(p['desc'], quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta property="article:published_time" content="{p['date']}">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="stylesheet" href="/assets/index-Bie2yWpX.css">
<style>{PAGE_CSS}</style>
<script type="application/ld+json">{ld}</script>
</head>
<body>
{nav_html()}
<main>
<article class="vp-wrap">
<p class="vp-eyebrow"><a href="/#blog">Blog</a></p>
<h1 class="vp-title font-display">{html.escape(p['title'])}</h1>
<p class="vp-meta"><time datetime="{p['date']}">{p['long']}</time><span aria-hidden="true"> &middot; </span>{p['read']} min read</p>
<div class="vp-cover"><img src="/blog/covers/{p['slug']}.svg" width="1200" height="750" alt=""></div>
<div class="vp-body">
{render(p['body'])}
</div>
<p class="vp-note">This article is general information for operators and is not legal advice. Regulatory requirements differ by market and change, so confirm current rules with your compliance team and counsel.</p>
</article>
<section class="vp-cta"><div class="vp-cta-in">
<p class="vp-eyebrow">Work with us</p>
<h2 class="font-display">Talk to us about your operation</h2>
<p>We work with operators, platforms and new ventures on exactly these questions. Tell us what you are dealing with and we will say whether we can help.</p>
<div class="vp-cta-btns"><a class="vp-btn" href="/#contact">Talk to us</a><a class="vp-btn vp-btn-o" href="{CAL}" rel="noopener" target="_blank">Book a call</a></div>
</div></section>
<nav class="vp-pns" aria-label="More posts">{pn('Newer', newer)}{pn('Older', older)}</nav>
</main>
{footer_html()}
<script>
(function(){{var b=document.getElementById('vp-menu-btn'),m=document.getElementById('vp-menu');if(!b||!m)return;
var ic=b.innerHTML,x='<svg width="22" height="16" viewBox="0 0 22 16" fill="none"><line x1="1" y1="1" x2="21" y2="15" stroke="currentColor" stroke-width="1.5"/><line x1="21" y1="1" x2="1" y2="15" stroke="currentColor" stroke-width="1.5"/></svg>';
function set(o){{m.hidden=!o;b.setAttribute('aria-expanded',o?'true':'false');b.innerHTML=o?x:ic}}
b.addEventListener('click',function(){{set(m.hidden)}});
m.addEventListener('click',function(e){{if(e.target.tagName==='A')set(false)}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')set(false)}});}})();
</script>
</body>
</html>
'''

for i, p in enumerate(posts):
    newer = posts[i - 1] if i > 0 else None
    older = posts[i + 1] if i + 1 < len(posts) else None
    d = os.path.join(ROOT, 'blog', p['slug']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(page(p, older, newer))

# /blog/ lands on the homepage section
open(os.path.join(ROOT, 'blog', 'index.html'), 'w').write('<!doctype html><html lang="en"><head><meta charset="UTF-8"><title>Blog | Verita IGAMING CONSULTANCY</title><link rel="canonical" href="%s/#blog"><meta http-equiv="refresh" content="0;url=/#blog"></head><body><a href="/#blog">Blog</a></body></html>\n' % SITE)

# ---------------------------------------------------------------- sitemap, robots, og images
urls = [f'{SITE}/'] + [f"{SITE}/blog/{p['slug']}/" for p in posts]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    lm = next((p['date'] for p in posts if u.endswith(f"/{p['slug']}/")), posts[0]['date'])
    sm += f'  <url><loc>{u}</loc><lastmod>{lm}</lastmod></url>\n'
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(sm + '</urlset>\n')
open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
try:
    import cairosvg
    for p in posts:
        cairosvg.svg2png(url=os.path.join(ROOT, 'blog', 'covers', p['slug'] + '.svg'), write_to=os.path.join(ROOT, 'blog', 'covers', p['slug'] + '.png'), output_width=1200, output_height=630)
except ImportError:
    print('cairosvg missing: OG png images not regenerated')

# ---------------------------------------------------------------- homepage bundle patch
data = [dict(slug=p['slug'], title=p['title'], desc=p['desc'], short=p['short'], read=p['read']) for p in posts]
BLOG_JS = '/*VBLOG-START*/var VBLOGS=' + json.dumps(data, ensure_ascii=False) + ''';function VBlogSection(){var P=VBLOGS;var card=function(p,i,feat){return (0,x.jsx)(T,{delay:feat?0:(i%3)*80,className:feat?"vb-cell vb-feat":"vb-cell",children:(0,x.jsxs)("a",{href:"/blog/"+p.slug+"/",className:"vb-card"+(feat?" vb-card-feat":""),children:[(0,x.jsxs)("span",{className:"vb-media",children:[(0,x.jsx)("img",{className:"vb-img",src:"/blog/covers/"+p.slug+".svg",alt:"",width:1200,height:750,loading:"lazy",decoding:"async"}),(0,x.jsx)("span",{className:"vb-shade"}),(0,x.jsx)("span",{className:"vb-meta",children:p.short+" \\u00b7 "+p.read+" min read"}),(0,x.jsxs)("span",{className:"vb-stack",children:[(0,x.jsx)("span",{className:"vb-title font-display",children:p.title}),(0,x.jsx)("span",{className:"vb-desc","aria-hidden":"true",children:p.desc})]})]}),(0,x.jsx)("span",{className:"vb-below",children:p.desc})]})},p.slug)};return (0,x.jsx)("section",{id:"blog",style:{borderTop:"1px solid var(--border)"},children:(0,x.jsxs)("div",{style:{maxWidth:1200,margin:"0 auto",padding:"120px 32px"},children:[(0,x.jsxs)(T,{children:[(0,x.jsx)("p",{style:{fontSize:11,letterSpacing:"0.2em",textTransform:"uppercase",color:"var(--accent)",fontWeight:600,marginBottom:14},children:"Insights"}),(0,x.jsx)("h2",{className:"font-display",style:{fontSize:"clamp(32px, 4vw, 52px)",lineHeight:1.1,letterSpacing:"-0.01em",marginBottom:20},children:"Blog"}),(0,x.jsx)("p",{style:{fontSize:17,lineHeight:1.7,color:"var(--muted-foreground)",fontWeight:300,maxWidth:560,marginBottom:56},children:"Notes for operators on retention, payments, onboarding, compliance and delivery."})]}),(0,x.jsx)("div",{className:"vb-grid",children:P.map(function(p,i){return card(p,i,i===0)})})]})})}/*VBLOG-END*/'''

js = open(BUNDLE, encoding='utf-8').read()
js = re.sub(r'/\*VBLOG-START\*/.*?/\*VBLOG-END\*/', '', js, flags=re.S)
assert 'function VSub(' in js
js = js.replace('function VSub(', BLOG_JS + 'function VSub(', 1)
js = js.replace('var C=[`What We Do`,`How We Work`,`Who We Serve`]', 'var C=[`What We Do`,`How We Work`,`Who We Serve`,`Blog`]')
SEC = '(0,x.jsx)(VBlogSection,{}),'
anchor = '(0,x.jsx)(`section`,{id:`contact`,'
if SEC + anchor not in js:
    assert js.count(anchor) == 1
    js = js.replace(anchor, SEC + anchor, 1)
FOOT_OLD = "(0,x.jsx)(S,{size:`sm`}),(0,x.jsx)(`p`,{style:{fontSize:12,color:`var(--muted-foreground)`},children:`© 2026 Verita IGAMING CONSULTANCY - UAE · LATAM · CYPRUS`})"
FOOT_NEW = ("(0,x.jsx)(S,{size:`sm`}),(0,x.jsx)(`nav`,{\"aria-label\":`Footer`,style:{display:`flex`,flexWrap:`wrap`,gap:`8px 24px`},children:[[`What We Do`,`#what-we-do`],[`How We Work`,`#how-we-work`],[`Who We Serve`,`#who-we-serve`],[`Blog`,`#blog`],[`Contact`,`#contact`]].map(function(l){return (0,x.jsx)(`a`,{href:l[1],className:`vp-flink`,style:{fontSize:12,letterSpacing:`0.08em`,textTransform:`uppercase`,color:`var(--muted-foreground)`,textDecoration:`none`},children:l[0]},l[0])})}),"
            "(0,x.jsx)(`p`,{style:{fontSize:12,color:`var(--muted-foreground)`},children:`© 2026 Verita IGAMING CONSULTANCY - UAE · LATAM · CYPRUS`})")
if FOOT_OLD in js:
    js = js.replace(FOOT_OLD, FOOT_NEW, 1)
else:
    assert 'vp-flink' in js, 'footer anchor not found'
open(BUNDLE, 'w', encoding='utf-8').write(js)

# ---------------------------------------------------------------- css
BLOG_CSS = open(os.path.join(SRC, 'blog.css')).read()
css = open(CSSF, encoding='utf-8').read()
css = re.sub(r'/\*VBLOG-CSS-START\*/.*?/\*VBLOG-CSS-END\*/', '', css, flags=re.S)
css = css.rstrip() + '\n/*VBLOG-CSS-START*/' + BLOG_CSS + '/*VBLOG-CSS-END*/\n'
open(CSSF, 'w', encoding='utf-8').write(css)
print('built', len(posts), 'posts')

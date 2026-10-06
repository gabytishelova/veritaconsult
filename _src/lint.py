import re,glob,sys
banned=r"\b(delve\w*|crucial\w*|robust\w*|landscape\w*|leverag\w*|unlock\w*|navigat\w*|journey\w*|game-changer\w*|seamless\w*|elevat\w*|empower\w*|foster\w*|pivotal\w*|harness\w*)\b"
pats=[("emdash","[—–]"),("emoji","[\U0001F300-\U0001FAFF☀-➿]"),("banned",banned),
("heres","here's the thing|here is the thing"),("realq","the real question"),
("contrast",r"\b(isn't|is not|aren't|are not|not just|not only|doesn't|does not)\b[^.\n]{0,80}\.\s*(It's|It is|They're|They are|That's)"),
("notbut",r"\bnot [^.,;\n]{1,40}, but\b"),("spaced-hyphen"," - "),("boldlabel",r"^[-*]\s*\*\*")]
tot=0
for f in sorted(glob.glob('posts/*.md')):
    t=open(f).read();head,body=t.split('\n\n',1)
    wc=len(re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',body).split())
    print(f,wc)
    for n,p in pats:
        for m in re.finditer(p,body,re.I|re.M):
            ln=body[:m.start()].count('\n')+1
            print('   ',n,'L%d'%ln,repr(body[max(0,m.start()-40):m.end()+40]))

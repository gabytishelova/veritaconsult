import re,sys,json
B='https://www.verita-consult.com/blog/'
P=[
("Why retention budgets leak","retention-budgets-leak","6 Oct 2026","Opinion",
"""Most retention budgets pay players to do what they were going to do anyway.

Send a 20% reload offer to everyone who lapsed for 10 days and the report will show thousands of returns. Hold back 10% of the audience and you will often find a large share of them came back without the offer. The campaign takes credit for those players, and the bonus cost is paid on them too.

A standing holdout costs a little revenue each month. It also tells you what every other number in the report means.

We wrote up where retention spend leaks and what to ask your team.""",""),
("Bonus economics: growth or subsidy","bonus-economics","22 Sep 2026","Scenario",
"""Say a player gets a bonus with a 30x wagering requirement. On a slot with a 4% house edge, the expected loss from clearing it is 120% of the bonus, so the offer pays for itself. Move the same player to a game with a 1% edge and the same terms cost you money.

The test is short. Wagering multiple times house edge has to be above 1. Game weighting is the control that keeps it true as your catalogue changes.

When did your team last check it?""","#iGaming"),
("The cashier is your conversion funnel","cashier-conversion-funnel","8 Sep 2026","Question",
"""What is your deposit approval rate by payment method and country this month?

If the answer takes a week to produce, there is probably revenue sitting in failed transactions. On 100,000 monthly attempts, five points of approval rate is 5,000 deposits. No acquisition campaign delivers that for the same effort.

The cashier is the last step of your conversion funnel and often the least measured. We wrote about what to track, how to weigh fees against approval rates, and who should own it.""","#iGaming #Payments"),
("KYC without killing the first deposit","kyc-onboarding-friction","25 Aug 2026","Opinion",
"""Regulators require identity checks. The speed of your review queue is your own decision.

If 30% of new registrations fall out of automated verification into a manual queue that averages 18 hours, many of those players are gone before anyone looks at them. Automated pass rate and queue time deserve the same attention as acquisition cost.

Document requests that appear for the first time at withdrawal belong on the same list. They drive complaints, and most of them can be avoided by asking earlier.

Our latest post covers where the friction sits and what to measure.""",""),
("Responsible gambling is a product capability","responsible-gambling-product","11 Aug 2026","Scenario",
"""Take a flagged player who receives a reload offer at 2 a.m. The alert fired, but it went to a compliance inbox. The CRM never heard about it.

That gap sits between the policy and the product. Player protection works when indicators are calculated in near real time, each one has a defined response, and the suppression flag reaches every marketing channel. It also needs end-to-end testing after each platform release, the same way you test a payment flow.

We wrote about building it as a product capability, with the UK customer interaction rules as an example.""","#ResponsibleGambling"),
("What decides the timeline in a new regulated market","new-regulated-market-timeline","28 Jul 2026","Opinion",
"""Ask how long a new market will take and you will hear the regulator's processing time. In the UK, the Gambling Commission publishes 16 weeks as the target for an operating licence application and says it is not guaranteed.

That number rarely sets the launch date. Bank accounts, platform certification, local payment methods, supplier approvals and local hiring tend to take longer. Draw the critical path with all of them on it and the licence is often not the constraint.""",""),
("Switching platform providers without losing players","platform-migration","14 Jul 2026","Question",
"""How many of your active players would notice if you changed platform provider tomorrow?

The target is close to none. Getting there depends on field-by-field data mapping, balances that match to the cent, self-exclusions and limits that carry over without a reset, and a rollback plan with a trigger you have tested.

Rehearse at least twice on production-sized data. Phase the cutover by brand, market or cohort where you can. Migration problems get found in rehearsal or found by players.""","#iGaming"),
("Tracking you can trust","tracking-you-can-trust","30 Jun 2026","Scenario",
"""Say marketing reports 4,200 new depositors, finance reports 3,900, and the affiliate network reports 4,600 and invoices for all of them.

Usually each is right about its own definition. Write down what counts as a new depositor, which time zone ends the day and which revenue figure the business calls revenue. Then reconcile weekly against platform records, not monthly.

A weekly check costs less than a quarterly argument.""",""),
("Fractional leadership or a full-time hire","fractional-vs-full-time-leadership","16 Jun 2026","Opinion",
"""Not every senior gap needs a full-time hire. If the problem has a shape and an end date, such as a market entry, a migration or a rebuilt retention function, interim leadership can start in weeks and leave behind a team, a plan and a brief for the successor.

If the role needs daily line management of a large team, hire for it.

Before you decide, write the 90-day outcome in one sentence. If you cannot, the problem is not ready for outside help.""",""),
("Why roadmaps stall between strategy and delivery","roadmaps-stall","2 Jun 2026","Question",
"""Why do roadmaps agreed in January look so thin by June?

Usually the plan adds up to more work than the teams can deliver. Say 40 initiatives and capacity for 12. Twenty-eight slip and nobody knows which in advance. The fix is arithmetic: count capacity in weeks per team, size every initiative in the same unit, stop when the total is reached and name what was dropped.

Then give each initiative one owner for the commercial result.""","#iGaming #Delivery"),
]
out=[]
bad=r"[—–]|\b(delve|crucial|robust|landscape|leverag|unlock|navigat|journey|game-changer|seamless|elevat|empower|foster|pivotal|harness)"
for t,s,d,f,body,tags in P:
    wc=len((body+'\n'+tags).split())
    flag=re.findall(bad,body+tags,re.I)
    print(wc,s,f,flag)
    assert 50<=wc<=150 and not flag
    out.append((t,s,d,f,body,tags))
json.dump(out,open('/tmp/claude-0/work/li.json','w'))
md=["# Verita LinkedIn Posts","","Ten posts, one per article, newest first. Each ends with the article link. Copy a post from its first line to the link.",""]
for i,(t,s,d,f,body,tags) in enumerate(out,1):
    md.append(f"## {i}. {t}"); md.append(f"Article date {d}. Format: {f}."); md.append("")
    md.append(body.replace("\n\n","\n\n"))
    md.append("")
    if tags: md.append(tags); md.append("")
    md.append(B+s+'/'); md.append("")
open('/tmp/claude-0/work/li.md','w').write("\n".join(md))

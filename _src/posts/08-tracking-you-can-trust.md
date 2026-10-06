title: Tracking you can trust
slug: tracking-you-can-trust
date: 2026-06-30
desc: When marketing, affiliates and finance report different numbers, the cause is usually definitions and timing. A reconciliation routine fixes most of it.

Marketing says 4,200 new depositors last month. Finance says 3,900. The affiliate network says 4,600 and wants commission on all of them. All three are probably right about their own definition.

The first job is to write the definitions down. Most disagreements start there.

What counts as a new depositor? First deposit attempted, first deposit successful, or first deposit that cleared with no chargeback? In which time zone does the day end? Is a player who registered in March and deposited in April a March acquisition or an April one? What happens to test accounts, staff accounts and accounts closed for fraud?

The same goes for revenue. Gross gaming revenue, net gaming revenue and net revenue after bonus costs and taxes are three different figures that people call revenue. Currency conversion adds another layer. Converted at the transaction date, the month-end rate or a fixed budget rate, the total changes. Bonuses, free spins and reversed withdrawals can all be booked at different times by different teams.

Put the definitions in one document, owned by finance, with examples. Every dashboard should state which definition it uses. This takes a week and ends most of the arguments.

After definitions, tracking itself.

Attribution windows. A player clicks an affiliate link on Monday, sees a social ad on Wednesday and registers on Friday through a search. Which channel gets the credit depends on the rule. Each platform applies its own, and each is generous to itself. If you add up the credit claimed by every channel, you get more depositors than you have.

Missing data. Browser privacy settings, ad blockers and consent choices remove a share of client-side tracking. The share varies by audience and device. Server-side tracking, where your platform sends the event directly, recovers part of it and is easier to audit. It has to be built and kept in step with the consent a player gave.

Late and duplicate events. Postbacks can arrive hours late or twice. A deposit counted twice in the affiliate system means a commission paid twice. Check how your platform handles retries and use a unique transaction ID on every event.

Identity. A player who registers on mobile and deposits on desktop may look like two people. Without a stable player ID passed across the steps, attribution breaks at that point.

Say an operator reconciles its affiliate report against the platform for one month and finds 6% of reported deposits have no matching transaction, mostly from duplicate postbacks and test traffic. That is a direct overpayment, and it was running every month before anyone compared the lists.

Cohort reporting adds another source of mismatch. Marketing counts by acquisition month. Finance counts by the month revenue was earned. A player acquired in January who generates revenue through the spring shows up in different places in each report. Both views are valid. The trouble starts when someone compares one team's January with another team's January and expects a match. Label every table with the basis it uses.

A routine that works is simple.

Pick a source of truth. For financial figures it is the finance ledger, fed by the platform. For player events it is the platform database. Everything else is a view that has to agree with it.

Reconcile weekly, not monthly. A small team can compare a short list: new depositors, deposits, GGR, bonus cost, by channel, between the platform, the marketing tool and the affiliate system. Differences above a set threshold get investigated. A weekly gap is easy to trace. A quarterly one rarely is.

Keep a log of changes. Tracking breaks when a developer changes a page, a tag manager is edited or a payment provider updates a callback. A record of what changed and when turns a mystery into a short search.

Treat affiliate disputes as data work. Give affiliates a clear statement of how you count a qualifying player, publish the rule, and settle against platform records. It protects both sides and keeps good partners.

A last note on privacy and consent. How you collect and use tracking data is regulated in many places, and rules differ. Your data protection lead and counsel need to approve the design of any tracking you add. Nothing here is legal advice.

Four questions for the team:

- Where are our definitions of new depositor and revenue written down, and who owns them?
- When did we last reconcile affiliate-reported deposits against platform records?
- What share of events is missing from client-side tracking, and what do we do about it?
- If finance and marketing disagree, who decides, and on what basis?

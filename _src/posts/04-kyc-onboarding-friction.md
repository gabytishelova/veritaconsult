title: KYC without killing the first deposit
slug: kyc-onboarding-friction
date: 2026-08-25
desc: Identity checks are mandatory, but how and when you run them is a product decision that moves first-deposit conversion.

Know your customer checks are not optional. The order in which you run them, the way you ask for documents and the speed of your review queue are all choices, and they move conversion.

Start with what the rules say, because the rules set the floor. The UK Gambling Commission's licence condition 17.1.1 says licensees must obtain and verify information in order to establish the identity of a customer before that customer is permitted to gamble. It names the minimum data as name, address and date of birth. The same condition limits when an operator can ask for more: a licensee cannot require additional documents as a condition of withdrawing funds if that information could reasonably have been obtained earlier. [The condition is published here](https://www.gamblingcommission.gov.uk/licensees-and-businesses/lccp/condition/17-1-1-customer-identity-verification).

Other regulators have their own requirements, and they change. Check the current text for each market with your compliance team and counsel. We are not giving legal advice here.

Within the rules, there is still a lot of room. Three places to look.

Automated pass rate. Most customers can be verified automatically from data providers, in seconds, with no upload. The share that pass automatically is the number to watch. If it is 70%, 30% of new registrations go to a slower path. Each point you add removes friction for hundreds of players a month. Pass rates differ by country and by provider, so they are worth comparing across at least two sources in each market.

The manual queue. Customers who fail the automated check wait for a person. Say an operator's review queue averages 18 hours with a long tail past two days. Many of those players try another site in the meantime. A queue that runs at 18 hours is a revenue problem with a staffing answer. Shift cover, clear rules for what an agent can decide alone and fast escalation for edge cases cut the time without cutting the standard.

The upload. A player who has to photograph a document on a phone, in poor light, through a form that crops the image badly, will give up. The capture step is a design problem. Guidance on screen, automatic edge detection and a clear explanation of why the check is needed all help. So does telling the player how long the review takes and sending a message when it is done.

Sequence is the other lever. Where the rules allow it, asking for the light checks first and the heavy ones later reduces drop-off at registration. Where the rules require verification before play, the aim is a single check that runs fast. For checks tied to source of funds or to higher thresholds, build the trigger on risk, not on a calendar. A customer who reaches a threshold should see a clear request the same day, not a surprise at the point of withdrawal.

Risk tiers help here. Low-risk registrations, such as a customer in a well-covered country with a clean automated match and a modest first deposit, can take the lightest route. Higher-risk signals, such as a mismatch in name data, a high-risk geography or a payment instrument in someone else's name, can trigger deeper checks. Each tier needs written rules that compliance has approved, so agents apply them the same way every time.

Withdrawal-stage document requests deserve a particular warning. They create complaints, chargebacks and bad reviews, and the licence condition above shows why regulators watch them. If your process regularly asks for documents at withdrawal that you could have asked for at deposit, the process needs changing, not the support script.

Measure the funnel in pieces. Registration to verification started. Started to automated pass. Automated pass or manual approval to first deposit. Time between each step. Break each by country, device and acquisition source, because they behave differently, and traffic from some affiliates will fail checks at much higher rates than the rest.

One more point on provider choice. A single verification vendor is a single point of failure and a single set of coverage gaps. A second vendor as fallback, called only when the first returns no match, raises pass rates in most markets without adding friction.

Name an owner for the whole path from registration to first deposit, across compliance, product and operations. Today it often has three owners and no one who sees the full drop-off.

Set targets for automated pass rate and for queue time, and review them monthly next to acquisition cost.

Four questions to put to your team:

- What share of new registrations pass automatically, by country?
- What is the median and the 90th percentile review time?
- At which step do we lose the most players, and why?
- How many withdrawal requests last month triggered a document request we could have made earlier?

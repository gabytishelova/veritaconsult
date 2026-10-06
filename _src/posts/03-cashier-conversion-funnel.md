title: The cashier is your conversion funnel
slug: cashier-conversion-funnel
date: 2026-09-08
desc: Failed deposits are lost revenue that never appears in a campaign report. Payment approval rates deserve the same attention as acquisition cost.

Every player you acquire has to get through the cashier. If the deposit fails, the acquisition cost is gone and the player is, in most cases, never seen again.

Most operators measure the funnel above the cashier closely. Click to registration, registration to verification, verification to deposit. The deposit step itself is often a single line in a report: deposits attempted, deposits succeeded. That ratio is where a lot of revenue goes missing.

Say an operator has 100,000 deposit attempts a month and 78% succeed. Raising that to 83% means 5,000 more successful deposits. At an average first deposit and a modest lifetime value, that is a significant sum every month. Nothing in the marketing plan produces that return for the same effort, and it comes with no extra acquisition cost.

Failed deposits have several different causes, and each has a different fix.

Issuer declines. The player's bank refuses the payment. The reasons vary by country and by card, and some of them depend on how the transaction is classified when it is sent. Merchant category codes, descriptors and the data fields passed to the processor all affect the outcome. Different processors get different approval rates on the same traffic, which is why routing matters.

Authentication. Strong customer authentication in Europe and similar checks elsewhere add a step. Some players abandon at that step, especially on mobile when they are sent to a banking app and do not come back. The design of the handoff matters as much as the rule behind it.

Method fit. A player arrives with a payment method the cashier does not offer, or offers on the third screen. Local methods carry most of the volume in many markets. A cashier built for a different country will lose players quietly.

Technical failures. Timeouts, provider outages and callbacks that arrive late. A deposit that succeeds at the bank but is not credited to the wallet for ten minutes creates a support ticket and a lost session.

Limits and rules. Minimum deposits, maximum deposits and regulatory limits that a player hits without a clear message about what went wrong.

The reporting that helps is more detailed than most dashboards. Approval rate by method, by country, by issuing bank group, by hour and by device. Decline reasons grouped and trended. Time from click to credited balance. Abandonment at each step inside the cashier. With that in front of you, patterns appear fast. One method failing for one bank group at night usually points to a processor issue you can raise with the provider the next morning.

Fixes that tend to pay off:

- Route each transaction to the processor with the best approval rate for that type of traffic, and have a second processor ready to take a retry.
- Order methods by market, with the local favourite first.
- Show a plain message after a decline that tells the player what to try next.
- Keep deposit and withdrawal limits visible before the player reaches them.

Fees and approval rates pull against each other, and the trade should be explicit. Say processor A charges 0.3 points less per transaction and approves 2 points fewer. On 100,000 monthly attempts, the cheaper option saves a small amount on fees and loses 2,000 deposits. The lost deposits are worth far more than the fee saving at almost any realistic average deposit. Finance teams that see only the fee line will choose A. Put both numbers on the same page.

Mobile adds its own friction. Wallets and banking apps open in another window, and the player has to return to your site afterwards. Test that return path on the phones your players use, on both operating systems. A flow that works on a desktop browser can lose a large share of mobile deposits at the return step.

There is a second half of the cashier that is easy to forget. Withdrawals. A player who gets paid out quickly and without a document request trusts the brand and deposits again. A player who waits five days does not. Withdrawal speed is a retention feature, and it belongs in the same review as deposits. It also sits next to onboarding checks, which we cover in the post on KYC.

Give payments a single owner who is accountable for approval rate and for net cost per transaction, including fees. Fee savings that lower approval rates are false savings. Test any change to routing on a share of traffic first.

Review provider contracts against actual performance. If the second processor outperforms the first on a market, that should change the volume allocation, and the contract should allow it.


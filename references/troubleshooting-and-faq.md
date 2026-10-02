# Troubleshooting and FAQ

> Generated from `docs/Spartan_Strategy_Partner_Guide.md` by `scripts/split_guide.py`. Edit the guide, not this file.

Contents: 13. Troubleshooting | 14. FAQ

---

## 13. Troubleshooting

| What you see | Likely cause | What to do |
|---|---|---|
| Balance shows 0 or "Queued for subscription" after subscribing | Subscriptions are processed at the next hourly Open Window | Wait for the next top of the hour |
| I cannot find the subscriber's money | It is in the Bot Account Funding wallet, not your Strategy Partner account | Log into the Bot Account, or use the transfer endpoint |
| Bot is not visible in the marketplace | You have not subscribed 100 USDT to your own bot yet, or it is private or not yet approved | Subscribe to your own bot; check the approval status and the public/private setting |
| I moved funds for a redemption but it did not pay out | A sweeper moved them back, the amount was too small for the user at the head of the queue, or NAV moved | Pause the sweeper, add a buffer, wait for the next batch |
| Pending Redemption is still above zero after I paid | New requests arrived, or the figure moved with NAV | Read the Console; clear the new total |
| The trade was profitable but my balance or NAV dropped | Entry timing at NAV, or fees and funding costs | See Scenarios A and B |
| My bot page ROI is lower than my Futures return | ROI is calculated on the whole pool, including idle Funding | Move idle Funding into Futures |
| I was approved but cannot find the next step | The Apply button became Console | Open the Console on the Open Platform page |
| I cannot see the Bot Account password | Google Authenticator is not bound yet | Bind it, then open the Account tab |
| I cannot withdraw from the Bot Account | Withdrawal is disabled by design | Redemptions go through the pool (Section 5 of `deposits-and-redemptions.md`) |
| An API call timed out; was the order placed? | Asynchronous API | Query the order or position before retrying (Section 7 of `api-and-bot-design.md`) |
| I hit a position limit on BTC or ETH | Standard contract limits | Use BTCSPARTANS or ETHSPARTANS |
| No profit share this week | NAV did not exceed the HWM, or settlement has not run | See Section 8 of `profit-share-and-tiers.md`; weekly settlement is Monday UTC+0 |
| A redemption has waited a long time | Not enough Funding, or risk was too high to release funds | Follow the playbook (Section 5.6 of `deposits-and-redemptions.md`); aim for 5 days |

---

---

## 14. FAQ

**Do I have to submit my strategy's source code?** No. You trade independently through the API or manually. The platform does not access your code or model parameters. It evaluates live trade execution and your NAV record.

**Does Spartan require exclusivity?** No. You can run the same strategy elsewhere.

**How many bots can I run?** 1 for Tier 1, up to 5 for Tier 5. Each bot keeps its own NAV and profit-share accounting.

**What is the minimum to launch?** 100 USDT of your own capital subscribed to your bot.

**What is the minimum a subscriber can put in?** Very small amounts, at the time of writing around 1 USDT. Check the bot page.

**Is there a minimum redemption or a redemption fee?** Not currently.

**Is there an AUM cap?** Not currently enforced.

**Can I use hedge mode and cross or isolated margin?** Yes to both.

**Can I withdraw my own principal?** Yes, through the same redemption rules, but it can lower your tier.

**What happens if my strategy underperforms?** No profit share is paid during a drawdown (HWM). Missing tier metrics can lead to a downgrade; new listings from external providers have a 60-day protection period.

**Do I get paid on the first day?** Only after settlement, and only above the HWM.

**Are the contract specs for TradFi the same as crypto?** Fees are the same (0.06% taker, 0.04% maker). Check each contract's own risk limits.

**Can I trade any token?** You can trade all listed pairs. For BTC, ETH and gold, use the Spartan pairs.

**Where is the API documentation?** https://doc.onebullex.com/#/

---

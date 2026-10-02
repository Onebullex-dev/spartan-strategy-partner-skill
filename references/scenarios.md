# Worked scenarios

> Generated from `docs/Spartan_Strategy_Partner_Guide.md` by `scripts/split_guide.py`. Edit the guide, not this file.

Contents: 12. Worked Scenarios

---

## 12. Worked Scenarios

All numbers are illustrative.

### A. The trade closed in profit, but one subscriber lost money

Subscribers buy and sell at the NAV of the moment, which already includes unrealized PnL.

| Step | Event | Pool value | Shares | NAV |
|---|---|---|---|---|
| 0 | A subscribes 1,000; the position opens | 1,000 | 1,000 | 1.00 |
| 1 | Position is +200 unrealized | 1,200 | 1,000 | 1.20 |
| 2 | B subscribes 1,200 at NAV 1.20 and gets 1,000 shares | 2,400 | 2,000 | 1.20 |
| 3 | Position falls to -100 unrealized | 2,100 | 2,000 | 1.05 |
| 4 | C subscribes 1,050 at NAV 1.05 and gets 1,000 shares | 3,150 | 3,000 | 1.05 |
| 5 | Position recovers and closes at take-profit (+100 versus entry) | 3,350 | 3,000 | 1.117 |

| Subscriber | Deposited | Value at the end | Result |
|---|---|---|---|
| A | 1,000 | 1,116.67 | +116.67 |
| B | 1,200 | 1,116.67 | -83.33 |
| C | 1,050 | 1,116.67 | +66.67 |

The trade made +100 and every fill was identical, yet B ended with a loss, because B bought in at the high NAV. This is the correct result of share-based accounting.

### B. The trade closed flat, but the existing holder lost

| Step | Event | Pool value | Shares | NAV |
|---|---|---|---|---|
| 0 | A subscribes 1,000; the position opens | 1,000 | 1,000 | 1.00 |
| 1 | Position is -100 unrealized | 900 | 1,000 | 0.90 |
| 2 | B subscribes 900 at NAV 0.90 and gets 1,000 shares | 1,800 | 2,000 | 0.90 |
| 3 | Position recovers and closes flat (0 PnL) | 1,900 | 2,000 | 0.95 |

A: 1,000 shares = 950 (deposited 1,000, so -50). B: 1,000 shares = 950 (deposited 900, so +50). The trade itself was flat. A subscriber who enters while a position is under water buys at a lower NAV and shares in the recovery. It does not matter whether B's money was still in Funding or already in Futures: B owns shares of the whole pool from the moment the subscription is processed.

### C. A deposit lands while your position is open

Futures 1,000. Your open position risks 10% (100). B subscribes 1,000, so the pool is now 2,000 and A and B each own 50%. If the position is stopped out for 100, each loses 50, not A losing 100. The existing position's result is now shared across the bigger pool, in both directions. When you then move B's 1,000 into Futures, your **next** trade sizes at 10% of 2,000 = 200. Moving funds changes the size of the next trade, not who owns the current one.

### D. Your bot is flat when someone redeems

Futures 3,000, Funding 0, no open positions. A subscriber requests 500. At the next hourly batch the system moves 500 from Futures to Funding and pays out at that moment's NAV. You need to do nothing.

### E. The queue and a request that does not fit

Positions are open. Funding holds 300. The queue is X 500, then Y 100, then Z 150. At the batch: X (500) is larger than 300, so X keeps waiting; Y (100) is paid, Funding is 200; Z (150) is paid, Funding is 50. X is still waiting and still shows as the longest wait. To clear X, move at least 500 (plus a small buffer) into Funding.

### F. A queue building over two days

- Day 1, 14:00: X requests 100. Email: 1 user, 100 pending, longest wait 0h.
- Day 1, 20:00: Y requests 400. Email: 2 users, 500 pending, longest wait 6h.
- Day 2, 10:00: you check your positions, risk is small. You pause your sweeper and move 520 (500 plus a buffer) from Futures to Funding.
- Day 2, 11:00: the hourly batch pays both. The Console shows Pending Redemption 0. No confirmation email is sent. You resume the sweeper.

### G. You withdraw your own principal

You are Tier 3 with 10,000 principal. You redeem 4,000 of it. Your principal is now 6,000, below the Tier 3 requirement of 10,000, so at the next tier review you can move down to Tier 2 (profit share, bot limit and settlement frequency change with it). Your own redemption goes through the same queue and NAV rules as any subscriber.

### H. A very large subscription arrives

An AUM cap is not currently enforced, so a 50,000 subscription into a 5,000 pool simply enters. Expect: your open positions are diluted (Scenario C); you must move the funds into Futures promptly; your next trades size about ten times larger, so check the contract's position limits and liquidity first; and a later large redemption is a large liquidity event you should plan for.

### I. You need margin urgently, and Funding holds money

Funding is not margin. If a position is close to liquidation, transfer Funding -> Futures immediately. If that money was set aside for pending redemptions, those redemptions will wait longer. Keep your BD or support informed if this delays them.

### J. The API is down while redemptions are pending

Keep the pending amount in Funding, de-risk where you can, and contact your BD or support early. Do not wait for day 5. Requests left unprocessed for an extended period can lead to platform risk-management measures.

---

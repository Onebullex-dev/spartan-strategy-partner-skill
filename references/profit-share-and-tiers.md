# Profit sharing, earnings and tiers

> Generated from `docs/Spartan_Strategy_Partner_Guide.md` by `scripts/split_guide.py`. Edit the guide, not this file.

Contents: 8. Profit Sharing and Earnings | 9. Tier System

---

## 8. Profit Sharing and Earnings

### 8.1 How You Earn

| Source | Notes |
|---|---|
| **Profit share** | A percentage of subscribers' profit above the High-Water Mark. Your main income. |
| **Referral rebate** | If a referral/partner relationship is set up with subscribers and a rebate rate is configured for you, you receive a share of the trading-fee rebate from their portion of the pool's volume. |
| **Subscription fee share** | Not currently enabled (subscription fees are waived during the promotional period). |

### 8.2 The High-Water Mark

Profit share is not paid just because the strategy is in profit. It is paid only when NAV per share rises above the highest NAV that has already produced profit share.

```text
NAV per share
 1.15 |                         *   new high: profit share only on 1.10 -> 1.15
 1.10 |        *------ HWM -----------------  previous high, already paid
 1.05 |                   *                   below HWM: no new profit share
 1.00 |  *
      +----------------------------------------------> settlements
```

After a drawdown the strategy must first recover and pass the old HWM. The same gain is never paid twice, and subscribers do not pay profit share during losses.

### 8.3 Settlement

Profit share is calculated at settlement on the strategy's actual net value: realized and unrealized PnL, trading fees, funding costs and other adjustments. Open positions are included, so settlement reflects the true position at that moment.

- **Weekly tiers:** settled every Monday (UTC+0).
- **Monthly tiers:** settled at the start of the month.
- Your payout is sent to your Strategy Partner account (Funding).

If the strategy's NAV at settlement does not exceed the HWM, no new profit share is generated for that period.

### 8.4 What You Actually Receive

The "Profit Sharing" percentage on the bot page is what subscribers pay. The platform usage fee is 10% of that profit share (1/10), deducted at settlement. If no profit share is generated in a cycle, no fee is charged. Subscribers' principal is not affected.

| Tier | Profit share (subscribers pay) | You receive | Platform fee |
|---|---|---|---|
| 1 | 10% | 9% | 1% |
| 2 | 12% | 10.8% | 1.2% |
| 3 | 15% | 13.5% | 1.5% |
| 4 | 17% | 15.3% | 1.7% |
| 5 | 20% | 18% | 2% |

Example (Tier 3): profit above the HWM at settlement is 10,000 USDT. Profit share 15% = 1,500. Platform fee 10% of that = 150. You receive 1,350, which is 13.5% of the profit.

### 8.5 Referral Rebate

Where a referral or partner relationship exists and a rebate rate is defined for you, the rebate is calculated from the trading fees paid by the bot in proportion to the referred user's share of the pool, and paid once a day.

```text
rebate = trading fee x (user's shares / total shares) x your rebate rate
```

For private bots, you can apply the partner relationship to whitelisted UIDs in the Users tab.

---

---

## 9. Tier System

Your tier sets your profit share, settlement frequency, bot limit and support level. Tiers are assessed on 30-day metrics, not on profit alone.

| | Tier 1 FIRST BLOOD | Tier 2 PROVEN IN BATTLE | Tier 3 ELITE GUARD | Tier 4 UNDYING FORCE | Tier 5 ETERNAL GLORY |
|---|---|---|---|---|---|
| Manager's capital | 100 | 1,000 | 10,000 | 50,000 | 150,000 |
| 30d ROI | -- | >= 0 | >= 0 | >= 0 | >= 0 |
| 30d max drawdown | -- | -- | <= 50% | <= 40% | <= 30% |
| 30d avg redemption time | <= 6 days | <= 5 days | <= 4 days | <= 4 days | <= 4 days |
| 30d volume | Unlimited | >= 100K | >= 500K | >= 2M | >= 5M |
| Profit distribution | Monthly | Monthly | Weekly | Weekly | Weekly |
| Bot limit | 1 | 2 | 3 | 4 | 5 |
| Profit sharing | 10% | 12% | 15% | 17% | 20% |
| Strategy provider fee (you receive) | 9% | 10.8% | 13.5% | 15.3% | 18% |
| Platform fee | 1% | 1.2% | 1.5% | 1.7% | 2% |
| Dedicated service | -- | -- | -- | -- | Yes |

- **AUM cap:** not currently enforced.
- **Manager's capital** is the money you subscribe into your own bot (principal capital). Reducing it can lower your tier.
- **Upgrades** apply when you meet a higher tier's requirements (the system checks daily at UTC+0 and when you add principal). **Downgrades** are reviewed on a recurring schedule.
- **Redemption speed counts.** Slow redemption processing lowers your tier metrics.

**Mandatory for every tier:** no forced liquidation, volume manipulation, wash trading, matched trading or data falsification; no major unresolved user complaints; position management and risk controls within platform requirements. Violations can lead to restricted upgrades, a downgrade, suspended profit sharing, restricted new subscriptions, or removal of the strategy.

**External strategy providers** with a proven live record elsewhere need not start at Tier 1. A temporary tier can be granted after review (for example Tier 3 for stable mid-level, Tier 4 for strong risk management, Tier 5 for top performers). It comes with a 60-day protection period: an interim review at day 30 and a formal tier decision at day 60 based on your actual performance on OneBullEx. During protection you are not downgraded for ordinary metric shortfalls, but serious violations can still lead to immediate action.

---

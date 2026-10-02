---
name: spartan-strategy-partner
description: Operating manual for running a strategy (bot) on OneBullEx Spartan, a pooled strategy-trading system. Use when building, reviewing, or debugging a trading bot or manual workflow for Spartan, or when answering questions about the Funding vs Futures wallets, shares and NAV, subscriptions and redemptions, the redemption queue, profit sharing and the high-water mark, tiers, the three account types (Normal, Strategy Partner, Bot Account), API and MCP integration cautions, risk limits and Spartan pairs, or why a subscriber's balance changed.
---

# Spartan Strategy Partner

Guidance for people (and AI assistants) building or running a strategy on OneBullEx Spartan. Spartan is a pooled system: all subscriber money is traded as ONE account and profit and loss are split by shares. The person running it (the Strategy Partner) manages the pool through the Bot Account, by API, manually, or via MCP.

## The model in 60 seconds

- **One pool, shares not dollars.** Nobody owns "their" money inside the pool. NAV per share = (Funding + Futures, including unrealized PnL) / total shares.
- **Two wallets.** Funding = money in and out, cannot trade, is not margin. Futures = margin and trading. The bot sizes risk from the Futures balance.
- **Three account types.** Normal, Strategy Partner (same login, upgraded), Bot Account (separate login per bot, trade-only, withdrawal disabled). Subscriber money lands in the Bot Account.
- **Deposits** are batched at the top of every hour, shares are issued at that moment's NAV, money lands in Funding. The Strategy Partner moves it to Futures (nothing does this automatically unless they build it).
- **Redemptions** are paid from Funding at the NAV of the hourly batch that executes them (not at request time). If the bot has no open positions the system handles it automatically. If positions are open, the manager decides when it is safe to move money Futures -> Funding.
- **Profit share** is paid only above the High-Water Mark, settled weekly (Mondays, UTC+0) or monthly by tier. Platform fee is 10% of the profit share payable.

## Rules you must not get wrong

1. Subscriber money is in the **Bot Account**, never in the Strategy Partner account. The Bot Account cannot withdraw, by design.
2. **Funding is not margin.** Only Futures can back positions and trade.
3. New deposits are **not** moved to Futures automatically. A sweeper is the user's own script or manual action.
4. Redemption queue: checked in order; a request larger than the Funding balance waits and the next is checked; no partial payment. Add a small buffer because NAV can move before the batch runs.
5. It is not automatic when positions are open because pulling margin from under an open position can lead to liquidation. Explain it with the example in `references/deposits-and-redemptions.md`.
6. Target: clear every redemption within **5 days**. Beyond that the platform may take risk-management measures.
7. A sweeper must not undo redemptions: avoid sweeping Funding -> Futures around :50 to :10, sweep at a fixed minute, and add a "redemption mode" (can be driven by `GET /v2/bot/redeeming-info`).
8. The API is **asynchronous**. A timeout is not proof of "no position". Use client order ids, query state before retrying, reconcile after every restart.
9. Entry timing matters: subscribers buy and sell at NAV including unrealized PnL, so a profitable trade can still produce a loss for one subscriber. This is not a bug (see `references/scenarios.md`).
10. Own capital counts toward the tier. Withdrawing principal can lower the tier.
11. For BTC, ETH and gold use BTCSPARTANS, ETHSPARTANS, XAUSPARTANS. Always check each contract's position limits before scaling.
12. A forced liquidation of the bot is a serious violation and hurts every subscriber.
13. Risk sizing, transfer automation, redemption handling and recovery from API failures are the **Strategy Partner's own design decisions and responsibility**. The platform provides no standard bot or sweeper.

## When asked to write automation (sweepers, bots, redemption handling)

- Frame it correctly: these are the user's own quant design decisions and responsibility, not something the platform solves for them.
- Before writing code, ask for (or explicitly state your assumptions about) the decisions in `references/api-and-bot-design.md`, Section 7.4: sizing base, redemption policy, transfer cadence, API failure policy, buffers, monitoring.
- Deliver templates with clearly marked decision points and conservative defaults. Do not describe code as "safe", "production-ready" or platform-approved.
- Never write logic that releases margin for a redemption without a risk check the user has chosen. Never treat an API timeout or empty response as "no position".
- Remind the user to test with small size first.

## Loading this skill from GitHub

If you were given this repository's link, you do not need to download anything. Start from this file, then fetch only the files you need from:

`https://raw.githubusercontent.com/Onebullex-dev/spartan-strategy-partner-skill/main/<path>`

For example `.../main/references/deposits-and-redemptions.md`. Use the table below to choose files.

## Which file to read

| Task | Read |
|---|---|
| What Spartan is, wallets, NAV, the three account types | `references/overview.md` |
| Onboarding, creating a bot, Bot Console metrics, bot closure, platform rights | `references/setup-and-bot-console.md` |
| Deposits, redemptions, queue logic, notifications, sweeper rules | `references/deposits-and-redemptions.md` |
| A manual trader's workflow and daily routine | `references/manual-trading.md` |
| Writing or reviewing a bot or script (design checklist, pseudocode) | `references/api-and-bot-design.md`, then `references/api/` and `references/mcp.md` |
| Earnings, high-water mark, fee table, tiers | `references/profit-share-and-tiers.md` |
| Pairs, limits, liquidation, fees, risk disclosure | `references/risk-and-pairs.md` |
| "Why did my balance change?" with numbers | `references/scenarios.md` |
| Symptoms and FAQ | `references/troubleshooting-and-faq.md` |
| Dates of rule changes, glossary, translation notes | `references/changelog-and-glossary.md` |

## How to answer

- Be concrete: say which wallet, which direction, and who acts (system, API trader, or manual trader).
- Ask whether the user is an **API trader or a manual trader** when it changes the answer.
- Use the worked numbers in `references/scenarios.md` when explaining entry timing or dilution.
- **Do not invent** endpoints, fees, limits, dates or response fields. The only endpoints documented here so far are `POST /v2/balance/transfer` and `GET /v2/bot/redeeming-info`. For anything else read `references/api/` if it has content, otherwise point to https://doc.onebullex.com/#/.
- Statements marked "currently" or "at the time of writing" can change. Say so, and refer the user to the latest official announcement. Official announcements always prevail over this skill.
- This is operating guidance, not investment advice. Never promise returns.

## Maintenance

The full human-readable guide is `docs/Spartan_Strategy_Partner_Guide.md` in the repository. The files in `references/` are generated from it by `scripts/split_guide.py`. `references/api/` and `references/mcp.md` are maintained by hand.

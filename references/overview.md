# Overview: the model, wallets and account types

> Generated from `docs/Spartan_Strategy_Partner_Guide.md` by `scripts/split_guide.py`. Edit the guide, not this file.

Contents: Spartan in 60 Seconds | 1. What Spartan Is | 2. Core Concepts | 3. The Three Account Types

---

## Spartan in 60 Seconds

**What it is.** Spartan is a pooled strategy-trading system (OneBullEx describes it as a "pooled-vault, fund-style" model). All subscriber money goes into ONE pool that you trade as a single account. Everyone owns shares of the pool, and profit and loss are split by shares. Nothing is copied into separate follower accounts, so there is no slippage gap between you and your subscribers: everyone gets the same fills.

```text
Subscribers (A, B, C ...)
      |  deposit (processed every hour)
      v
+--------------------------------------------------------------+
|                  BOT ACCOUNT  =  ONE POOL                    |
|                                                              |
|   +------------------+   you move   +--------------------+   |
|   |  FUNDING wallet  | -----------> |   FUTURES wallet   |   |
|   |  money in / out  | <----------- |   trading margin   |   |
|   |  (cannot trade)  |   you move   |  (bot trades here) |   |
|   +------------------+              +--------------------+   |
|                                                              |
|   Pool value = Funding + Futures   -->   NAV per share       |
+--------------------------------------------------------------+
      |  redemptions are paid out of Funding
      v
Subscribers cash out their shares
```

**The 12 things every Strategy Partner must know**

1. **One pool, shares not dollars.** Nobody owns "their" money inside the pool. Everyone owns a percentage (shares), and the value of a share is the NAV.
2. **Two wallets.** Funding = money in and out, cannot trade. Futures = trading margin, the only balance your bot or your manual orders can use. The pool is Funding + Futures together.
3. **Three account types.** Normal account, Strategy Partner account, Bot Account. Subscriber money lands in the Bot Account. The Bot Account cannot withdraw, by design (Section 3).
4. **Three ways to operate.** API, Manual (log into the Bot Account and trade like a normal account), or MCP (API-based). All three work on the same pool. Manual traders do the transfers and the redemption decisions themselves: Section 6 of `manual-trading.md` is written for you.
5. **New money lands in Funding. You move it to Futures.** Nothing does this for you unless you build it yourself.
6. **Redemptions are paid from Funding**, at the NAV of the moment the batch runs (not the moment of the request). If your bot has no open positions, the system handles it automatically. If positions are open, you decide when it is safe to move money from Futures to Funding.
7. **Clear every redemption within 5 days.** Beyond that the platform may step in. Faster processing also helps your tier metrics.
8. **Why it is not automatic:** your risk is sized against the Futures balance. Pulling margin out from under an open position can put it at risk of liquidation (Section 5.5 of `deposits-and-redemptions.md`).
9. **Entry timing matters.** Subscribers buy and sell shares at the current NAV, which includes unrealized PnL. A profitable trade can therefore give different subscribers different results. This is normal share accounting, not an error (Section 12 of `scenarios.md`).
10. **You earn profit share only above the High-Water Mark**, settled weekly or monthly depending on tier. You receive the tier's net percentage (9% to 18% of profit); the 10% platform fee on your profit share is already deducted (Section 8 of `profit-share-and-tiers.md`).
11. **Tiers 1 to 5.** More own capital plus risk, volume and redemption-speed metrics unlock a higher profit share, more bots, and weekly settlement. Withdrawing your own capital can lower your tier (Section 9 of `profit-share-and-tiers.md`).
12. **Risk basics.** Use the Spartan pairs for BTC, ETH and gold; build for an asynchronous API; a forced liquidation of your bot is treated as a serious violation (Section 10 of `risk-and-pairs.md`).

**Your operating loop**

```text
        +--> 1. Check Funding for new deposits ---+
        |                                         v
 5. Watch the Console / API                   2. Move Funding -> Futures
    (Pending Redemption)                          |
        ^                                         v
        |                              3. Trade; size risk from your equity
        |                                         |
        +------- 4. Redemption request? Decide when it is safe to release funds
```

**Key numbers**

| Item | Value |
|---|---|
| Deposit processing | Batched every hour (Open Window, top of the hour) |
| Redemption pricing | NAV at execution (hourly batch), not at request time |
| Redemption target | Clear within 5 days |
| Own capital to launch a bot | Minimum 100 USDT (you subscribe to your own bot) |
| Trading fees | 0.06% taker / 0.04% maker |
| Profit share (what subscribers pay) | 10% to 20% by tier; you receive 9% to 18% |
| Settlement | Weekly (Mondays, UTC+0) or monthly, depending on tier |
| Bots per partner | 1 to 5 by tier |
| AUM cap | Not currently enforced |
| Minimum redemption / redemption fee | None currently |

---

---

## 1. What Spartan Is

### 1.1 A Pool, Not Copy Trading

Traditional copy trading mirrors each trade into every follower's separate account. Spartan trades one pooled account.

| Traditional copy trading | Spartan pool |
|---|---|
| Each follower has their own account | One account for everyone |
| Followers can get different fills than the leader | Everyone gets the exact same fill |
| Dropped or partial orders (margin or leverage mismatch) | No dropped orders, the pool trades as one position |
| Follower results can drift from the leader | Results are split by share of one single outcome |
| Followers can exit or change positions at any moment | Subscriptions and redemptions follow fixed pool rules |

```text
TRADITIONAL COPY TRADING
  signal --> A's own account  (own fill, own slippage)  100    -> +10% = 110
         --> B's own account  (own fill, own slippage)  1,000  -> +10% = 1,100
         --> C's own account  (own fill, own slippage)  10,000 -> +10% = 11,000

SPARTAN POOL
  A:    100 --\
  B:  1,000 ---+--> ONE pool: 11,100, traded as ONE account (one fill, one price)
  C: 10,000 --/
                  Outcome split by share:  A = 0.9%   B = 9.0%   C = 90.1%
```

### 1.2 What You Can Trade

- **Crypto perpetual futures:** USDT-margined pairs across major assets.
- **TradFi perpetual futures:** USDT-settled pairs on U.S. equities (for example AAPL, NVDA, TSLA), selected international equities, index ETFs (QQQ, SPY), gold (XAU) and crude oil (CL).
- **Spartan-exclusive pairs:** BTCSPARTANS, ETHSPARTANS, XAUSPARTANS. These are built for large-pool execution and carry much higher risk limits than the standard pairs (Section 10 of `risk-and-pairs.md`).
- Both **cross and isolated** margin modes are available, and both **hedge** and **one-way** position modes. Hedging inside the pool is allowed.

Because the pool is one account, you can run a weighted multi-asset portfolio, not only a single mirrored instrument.

### 1.3 What Your Subscribers See

Subscribers browse the Spartan marketplace, open a bot page (ROI, NAV, AUM, risk tags, profit-share ratio), transfer money to their Spartans account, tick the Spartans Risk Disclosure, and subscribe. Their subscription is queued until the next Open Window. Under "My Subscriptions" they see their position and can request redemption at any time. Knowing this helps you answer their questions.

---

---

## 2. Core Concepts

| Term | Meaning |
|---|---|
| **Pool** | Everything in the Bot Account: Funding wallet + Futures wallet. |
| **Funding wallet** | Entry and exit wallet. Subscriptions land here, redemptions are paid from here. It cannot trade and is not margin. |
| **Futures wallet** | Trading wallet and margin. Your bot sizes risk from this balance. |
| **Share** | Your proportional ownership of the pool. |
| **NAV (per share)** | Pool total assets (Funding + Futures, including unrealized PnL) divided by total shares. |
| **Open Window** | The top of every hour, when queued subscriptions are converted to shares and redemptions are checked. |
| **High-Water Mark (HWM)** | The highest NAV per share that has already produced profit share. |
| **Principal capital** | The Strategy Partner's own money subscribed into the bot. |
| **Pending Redemption** | Total value of redemption requests waiting to be paid, shown in the Bot Console. |

The three formulas behind everything:

```text
NAV per share        = (Funding + Futures, incl. unrealized PnL) / total shares
Shares you receive   = deposit amount / NAV at the moment the subscription is processed
Value you cash out   = shares redeemed x NAV at the moment the redemption is processed
```

Example: pool 10,000, total shares 10,000, NAV 1.00. A subscriber deposits 1,100 when NAV is 1.10 and receives 1,000 shares. Later, when NAV is 1.20, redeeming those 1,000 shares pays 1,200.

---

---

## 3. The Three Account Types

This is the most common point of confusion for new Strategy Partners. Read it before anything else.

```text
 Normal account                (your original login)
      |  approved as Strategy Partner
      v
 Strategy Partner account      (same login, upgraded)
   - manages the strategy, subscribes to your own bot, receives profit share
   - withdrawal: enabled
      |  creates / you log into
      v
 Bot Account(s)                (separate login for each bot)
   - exclusively executes trades
   - withdrawal: DISABLED
   <-- subscriber money lands here
```

| | Normal account | Strategy Partner | Bot Account |
|---|---|---|---|
| Origin | Default when you sign up | Your Normal account, upgraded after approval | Generated by the system when a bot is approved |
| Login | Your email and password | Same as Normal | **Separate credentials**, shown in the Bot Console (Account tab) |
| Purpose | Standard platform use | Manage the strategy, subscribe to your own bot, receive profit share | **Exclusively executes trades** |
| Withdrawal | Enabled | Enabled | **Completely disabled at the architecture level** |
| Receives subscriber money | No | No | **Yes, directly** |
| Wallets | Standard | Standard | Funding and Futures |

What this means in practice:

- **Subscriber money is in the Bot Account**, never in your Strategy Partner account. If you are looking for a deposit, look there.
- To trade manually you log into the **Bot Account** with its own credentials. If you run several bots, each has its own login.
- The Bot Account cannot withdraw. Trade execution is isolated from fund custody: even someone who gained access to a Bot Account could not move subscriber money out. All exits go through the redemption path in Section 5 of `deposits-and-redemptions.md`.
- Your own principal and your profit share payouts live in your Strategy Partner account.
- After your application is approved, the old **Apply** button on the Open Platform page becomes **Console**. There is currently no separate notification. If you cannot find the next step, look for Console.
- Tip: keep a small personal note of which login belongs to which account type and which bot. The platform does not yet color-code them.

---

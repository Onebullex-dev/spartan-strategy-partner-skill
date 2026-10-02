# Spartan Strategy Partner Guide

*The complete operating manual for running a strategy on OneBullEx Spartan, for API traders and manual traders.*

Version: October 2026 | Applies to: Spartan pooled strategy bots on OneBullEx
Official API documentation: https://doc.onebullex.com/#/ . The full Open API V2 reference and the MCP guide (English and Chinese) are included in this repository: https://github.com/Onebullex-dev/spartan-strategy-partner-skill/tree/main/references/api
If anything in this guide conflicts with an official OneBullEx announcement, the announcement prevails (see Section 15 for the change timeline).

## How to Use This Guide

| If you are... | Read |
|---|---|
| New and in a hurry | "Spartan in 60 Seconds", then Section 3 (Account Types) |
| A manual trader | Sections 5, 6, 12 |
| An API / algo trader | Sections 5, 7, 10, 12 |
| Asking "why did my balance change?" | Sections 12 (Scenarios) and 13 (Troubleshooting) |
| Looking for earnings and tiers | Sections 8 and 9 |

## Table of Contents

- [Spartan in 60 Seconds](#spartan-in-60-seconds)
- [1. What Spartan Is](#1-what-spartan-is)
- [2. Core Concepts](#2-core-concepts)
- [3. The Three Account Types](#3-the-three-account-types)
- [4. Getting Started and Bot Setup](#4-getting-started-and-bot-setup)
- [5. Wallets, Deposits and Redemptions](#5-wallets-deposits-and-redemptions)
- [6. For Manual Traders](#6-for-manual-traders)
- [7. For API Traders and Bot Builders](#7-for-api-traders-and-bot-builders)
- [8. Profit Sharing and Earnings](#8-profit-sharing-and-earnings)
- [9. Tier System](#9-tier-system)
- [10. Risk, Pairs and Execution](#10-risk-pairs-and-execution)
- [11. Bot Closure and Platform Rights](#11-bot-closure-and-platform-rights)
- [12. Worked Scenarios](#12-worked-scenarios)
- [13. Troubleshooting](#13-troubleshooting)
- [14. FAQ](#14-faq)
- [15. Change Timeline](#15-change-timeline)
- [16. Glossary and Translation Notes](#16-glossary-and-translation-notes)

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
4. **Three ways to operate.** API, Manual (log into the Bot Account and trade like a normal account), or MCP (API-based). All three work on the same pool. Manual traders do the transfers and the redemption decisions themselves: Section 6 is written for you.
5. **New money lands in Funding. You move it to Futures.** Nothing does this for you unless you build it yourself.
6. **Redemptions are paid from Funding**, at the NAV of the moment the batch runs (not the moment of the request). If your bot has no open positions, the system handles it automatically. If positions are open, you decide when it is safe to move money from Futures to Funding.
7. **Clear every redemption within 5 days.** Beyond that the platform may step in. Faster processing also helps your tier metrics.
8. **Why it is not automatic:** your risk is sized against the Futures balance. Pulling margin out from under an open position can put it at risk of liquidation (Section 5.5).
9. **Entry timing matters.** Subscribers buy and sell shares at the current NAV, which includes unrealized PnL. A profitable trade can therefore give different subscribers different results. This is normal share accounting, not an error (Section 12).
10. **You earn profit share only above the High-Water Mark**, settled weekly or monthly depending on tier. You receive the tier's net percentage (9% to 18% of profit); the 10% platform fee on your profit share is already deducted (Section 8).
11. **Tiers 1 to 5.** More own capital plus risk, volume and redemption-speed metrics unlock a higher profit share, more bots, and weekly settlement. Withdrawing your own capital can lower your tier (Section 9).
12. **Risk basics.** Use the Spartan pairs for BTC, ETH and gold; build for an asynchronous API; a forced liquidation of your bot is treated as a serious violation (Section 10).

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
- **Spartan-exclusive pairs:** BTCSPARTANS, ETHSPARTANS, XAUSPARTANS. These are built for large-pool execution and carry much higher risk limits than the standard pairs (Section 10).
- Both **cross and isolated** margin modes are available, and both **hedge** and **one-way** position modes. Hedging inside the pool is allowed.

Because the pool is one account, you can run a weighted multi-asset portfolio, not only a single mirrored instrument.

### 1.3 What Your Subscribers See

Subscribers browse the Spartan marketplace, open a bot page (ROI, NAV, AUM, risk tags, profit-share ratio), transfer money to their Spartans account, tick the Spartans Risk Disclosure, and subscribe. Their subscription is queued until the next Open Window. Under "My Subscriptions" they see their position and can request redemption at any time. Knowing this helps you answer their questions.

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
- The Bot Account cannot withdraw. Trade execution is isolated from fund custody: even someone who gained access to a Bot Account could not move subscriber money out. All exits go through the redemption path in Section 5.
- Your own principal and your profit share payouts live in your Strategy Partner account.
- After your application is approved, the old **Apply** button on the Open Platform page becomes **Console**. There is currently no separate notification. If you cannot find the next step, look for Console.
- Tip: keep a small personal note of which login belongs to which account type and which bot. The platform does not yet color-code them.

---

## 4. Getting Started and Bot Setup

### 4.1 Onboarding Steps

1. **Register** on OneBullEx (email and password, optional referral code from your BD).
2. **Apply** on the Open Platform page (Apply Now). Describe your use case and trading style and leave a contact. Roles: quantitative firm (API), copy trader (manual), KOL/partner. Review takes about 1 to 3 business days.
3. **Approval.** The Apply button becomes Console.
4. **Create your bot** in the Bot Console (Create BOT), then submit for review.
5. **Bot approval.** Your bot gets its management tabs and a Bot Account.
6. **Subscribe to your own bot** (minimum 100 USDT) from your Strategy Partner account through the Spartan marketplace. Transfer funds to your Spartans account first. This is your principal capital, and it is required before the bot becomes publicly searchable.
7. **Move funds** from Funding to Futures in the Bot Account (manually or through the API transfer endpoint). Subscriptions process hourly, so a 0 balance right after subscribing is normal ("Queued for subscription").
8. **Start trading** by API, manually, or via MCP.

### 4.2 Creating a Bot

| Field | Rules |
|---|---|
| Strategy type | **Public:** any user can subscribe. **Private:** only whitelisted users you invite (by UID). |
| Bot name | English letters only, no spaces. |
| Strategy tags | Risk style (Aggressive, Steady, Conservative) and strategy type (for example mean reversion, trend following). |
| Description | Explain your strategy for subscribers. |

After submission the bot goes through review. Bot information currently cannot be edited by the manager after approval, so check your name, tags and description before submitting.

### 4.3 The Five Tabs of an Approved Bot

| Tab | What it contains |
|---|---|
| **Data** | Bot data and FAQ. Profit details are planned. |
| **Account** | Bot UID, the Bot Account's login email (virtual) and password. You must bind Google Authenticator before the password is shown. Use this to trade manually. |
| **API** | API Key, Secret Key, and links to Quick Start, API Reference and code examples. |
| **Bot Info** | The bot's public information (currently read-only). |
| **Users** | Subscribers, their subscription amounts and PnL. For private bots: the whitelist (enter UIDs, apply partner relationship). Only whitelisted users can subscribe to a private bot. |

### 4.4 The Bot Console

The Console is where you see what needs your attention.

| Metric | Meaning |
|---|---|
| Total Profit Distributed | Profit share paid out to you so far |
| Estimated Next Profit Distribution | Expected next payout, shown with the platform fee |
| Pending Redemption | Total value waiting to be redeemed (at current share value) |
| Pending Duration | How long the longest-waiting request has been waiting |
| Per bot: asset size (AUM), profit distributed, estimated next distribution, pending redemption, waiting time | The same figures for each of your bots |

The Console shows pending redemptions live. They are also emailed to you, and your code can read the same queue summary from the API (Section 5.4).

### 4.5 Three Ways to Operate

| Method | How it works |
|---|---|
| **API** | Trade with your bot's API Key and Secret Key. Full documentation: https://doc.onebullex.com/#/ (also in this repository: https://raw.githubusercontent.com/Onebullex-dev/spartan-strategy-partner-skill/main/references/api/openapi-en.md) |
| **Manual** | Log into the Bot Account and trade as you would on a normal futures account. You see Funding and Futures in one place. |
| **MCP** | A protocol-based way to connect, effectively a form of API trading. Described in the API documentation. |

Account transfers (Funding <-> Futures) can be done through the API: `POST /v2/balance/transfer` (see the "Fund Account" section of the API documentation).

---

## 5. Wallets, Deposits and Redemptions

This is the core of Spartan and the source of most support questions.

### 5.1 Funding Is Not Margin

The Bot Account works like a normal exchange account. Money in the Funding wallet does not back your positions. Your margin is in the Futures wallet. Funding still counts toward the pool value (NAV and ROI), but it cannot prevent a liquidation. If a position urgently needs margin, you must transfer Funding -> Futures yourself.

### 5.2 How Deposits Work

```text
Subscriber           Settlement account              Bot Account
    |  1. subscribes        |                             |
    |---------------------->|  (queued: "Queued for subscription")
    |                       |                             |
    |            2. next Open Window (top of the hour):   |
    |               shares issued at that moment's NAV    |
    |                       |---------------------------->|  money lands in FUNDING
    |                                                     |
    |                                 3. YOU move Funding -> Futures
    |                                    (manual, API, or your own script)
```

- Subscribers can submit at any time. Shares are issued at the next Open Window at that moment's NAV.
- From that moment the subscriber owns shares of the **whole pool**, including any position that is open right now. It does not matter whether their money is still in Funding or already in Futures.
- Moving the money to Futures does not change their ownership. It changes what your bot can use for its **next** trade.

### 5.3 How Redemptions Work

```text
Subscriber requests redemption
        |
        v
You are notified (Console + email, up to hourly while requests are pending)
        |
        v
Hourly batch (a window of about 10 minutes around the top of the hour, ~:55 to :05)
        |
        +-- Bot has NO open positions?
        |       YES --> the system moves the needed amount Futures -> Funding
        |               and pays out automatically at that moment's NAV
        |
        +-- Bot HAS open positions. Next user in the queue:
                Is this user's amount <= Funding balance?
                  YES --> paid out at that moment's NAV; Funding reduces by that amount
                  NO  --> this user keeps waiting; the next user in line is checked
                          |
                          +--> you decide: move Futures -> Funding when it is safe,
                               or reduce / close positions first.
                               Target: clear within 5 days.
```

Rules to remember:

- **Priced at execution.** The user receives shares x NAV at the moment the hourly batch executes, not at the moment they asked. NAV can move in between.
- **Queue order.** Requests are checked in order. A request that is larger than the current Funding balance waits, and the system moves on to the next one. There is no partial payment of a single request.
- **Flat bot = automatic.** If you hold no open positions, you do not need to do anything. The system draws from Futures and pays out at the next batch.
- **Add a small buffer.** Because the amount shown in the email is at the current share value and NAV may change before the batch runs, put in slightly more than the pending total.
- **Funds must still be there at the batch.** Money you place in Funding for exits has to stay in Funding until the hourly batch has run.

### 5.4 Notifications

- **Bot Console:** live view of Pending Redemption and Pending Duration.
- **Email:** sent while requests are pending and can arrive frequently (up to hourly). It shows three things: how many users are waiting, the total pending amount at the current share value, and how long the longest-waiting request has waited. It is a running status, not one email per request.
- **There is no "completed" email.** When Pending Redemption in the Console drops to zero, that batch is cleared. A new figure a minute later usually means a different, new request.
- **API:** `GET /v2/bot/redeeming-info` returns the redemption queue summary (no request parameters). Your bot can poll it instead of waiting for the email, for example to switch on a "redemption mode" or to raise an alert. See the API reference for the response fields.

### 5.5 Why It Is Not Automatic When Positions Are Open

The bot sizes its risk from the **Futures** balance, because that is the real margin account.

```text
Before:  Futures 10,000 | open position risk 1,000  = 10% of Futures
If 5,000 is pulled out while the position is still open:
         Futures  5,000 | same position risk 1,000  = 20% of Futures
```

The position does not shrink when margin leaves. With cross margin especially, taking margin out from under an open position can lead to liquidation before the stop-loss is reached. That can happen at night while you sleep, and it would hurt everyone still in the pool, including the person who asked to exit.

So you act like a portfolio manager:

- Risk is small and safe right now: release the funds and let them exit.
- Risk is large or concentrated: wait for positions to close, reduce them, or close them yourself, then release the funds.

You can normally move only the available (unused) balance. To release more, reduce or close positions to free margin.

### 5.6 Redemption Playbook

1. Open the Console. Read the pending total, number of users and longest wait.
2. Look at your open positions. How much would your risk change if that amount left Futures?
3. If it is safe: if you run an automatic Funding -> Futures sweeper, pause it first, then move the pending total (plus a small buffer) from Futures to Funding.
4. If it is not safe: reduce or close positions, or wait for them to close, then do step 3.
5. Let the next hourly batch run. The system pays out automatically.
6. Check the Console. When Pending Redemption is zero, resume your sweeper.
7. Do this well inside the 5-day target. Do not wait for day 5.

### 5.7 If You Automate Transfers

You can script Funding -> Futures. Whether to automate, and how, is your own design decision and responsibility; there is no standard sweeper to rely on. If you do automate, account for one rule: **do not let it undo your redemptions.** If a script instantly sweeps everything from Funding to Futures, money you placed in Funding for exits is pulled back before the hourly batch pays it out.

- Avoid sweeping during the redemption window (roughly :50 to :10). Many bots sweep at a fixed time such as :30 past the hour, and every few hours rather than continuously.
- Choose the cadence deliberately. A slower sweep leaves new deposits idle in Funding for longer.
- Add a "redemption mode" flag that pauses the sweeper while you are clearing a queue. You can set it by hand, or switch it automatically when `GET /v2/bot/redeeming-info` shows a pending queue.
- Use the transfer endpoint `POST /v2/balance/transfer` for both directions.

### 5.8 The 5-Day Rule

Aim to clear every redemption within 5 days. If requests stay unprocessed for an extended period, the platform may take risk-management measures to protect participants, such as reducing positions, partially closing positions, or ending the trading cycle. Redemption processing time is also one of your 30-day tier metrics (Section 9).

---

## 6. For Manual Traders

If you trade through the Bot Account login, you run the pool by hand. Everything in Section 5 applies to you, and you do these jobs yourself.

### 6.1 What Is Different From Trading Your Own Account

- The money is not only yours. Subscribers own shares and can request an exit at any time.
- New money does not appear in Futures on its own. It arrives in Funding.
- Your risk percentage should be based on the pool, so the money has to be in Futures.
- Redemption emails and the Console are part of your trading day.
- Subscribers enter and leave at NAV, which includes your unrealized PnL.

### 6.2 Your Session

Log into the Bot Account with the credentials from the Account tab (bind Google Authenticator first). You see both Funding and Futures in one place, can transfer between them, and can trade all supported pairs.

### 6.3 Sizing Risk From the Whole Pool

If you want to risk a fixed percentage of the pool, put the pool in Futures first.

```text
Funding 2,000 (new deposits) + Futures 8,000 = pool 10,000
Risking 1%:  before transfer = 1% of 8,000  = 80   (understates your intended risk)
             after transfer  = 1% of 10,000 = 100
```

Because your reported ROI is calculated on the whole pool, leaving large amounts idle in Funding also lowers your reported return.

### 6.4 Daily Routine

1. Check Funding for new deposits and move them to Futures.
2. Check the Console for Pending Redemption and Pending Duration.
3. Decide how to handle any pending redemption (Section 6.5).
4. Trade, sizing risk from the current pool.
5. Before you go offline, review open risk (Section 6.6).

### 6.5 Handling a Redemption Request

| Situation | What to do |
|---|---|
| No open positions | Nothing. The system pays out automatically at the next batch. |
| Open positions, risk small after the transfer | Move the pending total (plus a small buffer) from Futures to Funding. |
| Open positions, risk would become too high | Reduce or close positions, or wait for them to close, then move the funds. |
| Request is getting old | Prioritize it. Aim to clear inside 5 days. |

### 6.6 Before You Go Offline

- Is your open risk small enough that a redemption-sized transfer would not endanger it?
- Do your positions have stop-losses?
- Requests keep queuing while you are away. If you will be unavailable for more than a day or two, tell your BD or support.

### 6.7 Common Mistakes

- Leaving deposits in Funding for days.
- Moving margin out from under a large open position to pay a redemption.
- Ignoring the emails because "the system will handle it".
- Sizing risk from Futures while a large idle balance sits in Funding.

---

## 7. For API Traders and Bot Builders

> **Your responsibility.** This section explains how the system behaves and what your design has to account for. How you size risk, automate transfers, handle redemptions and recover from API failures is your own design decision and your responsibility as a quant. OneBullEx does not provide a standard bot or sweeper, and nothing here guarantees that a particular design is safe.

### 7.1 What the API Gives You

The API covers trading, balances, positions and account transfers (reference: https://raw.githubusercontent.com/Onebullex-dev/spartan-strategy-partner-skill/main/references/api/openapi-en.md, Chinese: https://raw.githubusercontent.com/Onebullex-dev/spartan-strategy-partner-skill/main/references/api/openapi-zh.md; live version: https://doc.onebullex.com/#/). For MCP see https://raw.githubusercontent.com/Onebullex-dev/spartan-strategy-partner-skill/main/references/api/mcp-en.md. The redemption queue summary is available at `GET /v2/bot/redeeming-info` (no request parameters), so your code can see pending redemptions without relying on the Console or email. You can build whatever mechanism you prefer on top of it, for example an automatic redemption mode, an alert, or fully automated handling. The Console and email still work alongside it.

### 7.2 Bot Design Checklist

1. **Define your sizing base.** Decide whether you size from Futures equity or from the pool total (Funding + Futures). Platform NAV and ROI use the pool total. If you size from Futures only, keep idle Funding small or read both balances.
2. **Re-read equity before every new position.** The pool changes through deposits, redemptions and PnL. A fixed lot size or a fixed assumed balance will drift away from your intended risk.
3. **Treat redemptions as normal events.** Cap your open risk so that a plausible redemption-sized transfer out of Futures does not endanger your positions.
4. **Design the sweeper carefully.** Fixed minute of the hour, not continuous; pause it while clearing redemptions (Section 5.7).
5. **Build for an asynchronous API.** Responses can be delayed and the server can have brief downtime. A timeout is not proof that nothing happened.
6. **Never assume "no response = no position".** On an error or timeout, query the order and position state before sending anything new.
7. **Use idempotent orders.** Give every order a client order id, and check by id before retrying so you never double-submit.
8. **Reconcile on start.** After every restart, reconcile open orders and positions before taking any action.
9. **Protect exits.** Take-profit and stop-loss orders can be delayed or missed in the same way. Verify they were accepted and re-check them.
10. **Respect rate limits** in the API documentation and use back-off on retries.
11. **Set margin and position modes explicitly** (cross or isolated, hedge or one-way) at startup and verify them per symbol.
12. **Use the right pairs and check limits.** Use BTCSPARTANS, ETHSPARTANS and XAUSPARTANS for those assets. Check each contract's maximum position size by leverage tier before scaling.
13. **Protect your keys.** Store the Secret Key in a secrets manager, never in source control, rotate it if it may have been exposed, and check the API documentation for any key restrictions that are available.
14. **Monitor.** Alert on low Futures balance, large idle Funding, margin ratio, API error rate, stale transfers, and a growing redemption queue (poll `GET /v2/bot/redeeming-info`).
15. **Test small.** Expect live results to differ from a backtest: deposits and redemptions change the pool while trades are open (Section 12).

### 7.3 An Example Loop (Pseudocode, Illustrative Only)

This is a sketch to show the moving parts, not a ready-made or recommended solution. Decide each step for your own strategy (see Section 7.4).

```text
every few minutes:
    info = GET /v2/bot/redeeming-info
    redemption_mode = (info shows a pending queue)   # or set by hand

every N hours, at a fixed minute (e.g. :30):
    if redemption_mode == ON:  skip
    funding = get_balance(FUNDING)
    if funding > min_sweep:    transfer(FUNDING -> FUTURES, funding)

before opening a position:
    equity = read current equity (Futures, or Funding + Futures)
    size   = risk_pct * equity / stop_distance
    verify available margin and the contract's position limit

on order submit:
    send with a client order id
    on timeout/error -> query order and position state first, never blind-retry

on restart:
    reconcile open orders and positions before any new action
```

### 7.4 Decisions That Are Yours

Before you run anything live, decide and write down your answers. There is no single right answer, and they should be revisited as your AUM grows.

- **Sizing base.** Do you size from Futures equity or from the pool total? How often do you re-read it, and what happens if the read fails?
- **Redemption policy.** When do you release funds? How much open risk are you willing to carry? What is the largest redemption you can absorb? Who decides: you, your script, or both?
- **Transfer automation.** Do you sweep Funding -> Futures at all? At what cadence and at which minutes? What happens if the sweeper fails or stops?
- **Failure policy.** What do you do when the API times out, errors, or is down? How do you query the real state, how many retries do you allow, when do you stop trading, and what is a safe state for your strategy?
- **Buffers and limits.** What margin buffer do you keep against liquidation? What are your maximum position sizes per contract?
- **Monitoring and override.** What do you watch, who is alerted, and how do you take manual control?
- **Rollout.** How do you test, and how do you scale from small size?

These are quant design decisions. Plan them yourself.

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

## 10. Risk, Pairs and Execution

### 10.1 Use the Spartan Pairs

For Bitcoin, Ethereum and gold, trade BTCSPARTANS, ETHSPARTANS and XAUSPARTANS rather than the standard contracts. Their risk limits are much higher (currently about 8x the standard pairs) because they are built for large pools. A pool that grows past the standard pair's limit cannot add positions.

### 10.2 Always Check the Contract's Risk Parameters

Before taking size on any pair, check its maximum position size at your intended leverage. Limits differ by pair, so do not assume they are uniform. A large pool takes large risk, and the contract has to allow it.

### 10.3 Liquidity Differs by Pair

Order book depth varies across pairs. Check depth before scaling, start small, and watch slippage on thinner pairs. The Spartan pairs and major TradFi pairs are built for size.

### 10.4 Cross Margin and Redemptions

If you hold large cross-margin positions for days, remember that subscribers can request an exit at any time. Keep risk modest enough that moving a redemption-sized amount out of Futures does not threaten your positions (Section 5.5).

### 10.5 Liquidation Is a Serious Event

A forced liquidation of your bot hurts every subscriber in the pool and counts as a serious risk event under the tier rules (Section 9). Size and protect positions accordingly.

### 10.6 Fees and ROI

Trading fees are 0.06% taker and 0.04% maker, the same for crypto and TradFi pairs. Fees generated by Spartan bots can qualify for rebates through the partner rebate system. Your displayed ROI is calculated on the whole pool (Funding + Futures), so money idle in Funding lowers it.

### 10.7 Risk Disclosure

Subscribers must accept the Spartans Risk Disclosure before subscribing. Cryptocurrency derivatives involve substantial risk, including extreme volatility, leverage and liquidation risk, liquidity risk, and the risk of strategy failure. Past performance does not guarantee future results.

---

## 11. Bot Closure and Platform Rights

- **Closing a bot.** A bot is removed once it has been liquidated, meaning its positions are closed and its subscribers have been redeemed. To retire a bot on purpose, contact your BD or support. Do not simply stop trading, because subscribers remain in the pool.
- **Platform rights.** To protect participants' funds and system stability, the platform reserves the right to take measures where needed, for example restricting new subscriptions, pausing a bot, reducing or closing positions, liquidating the bot, or removing it from the platform. Typical triggers are redemptions left unprocessed for an extended period, serious rule violations, risk events, or being unable to reach the manager.
- **Responsibility.** You operate your strategy with full autonomy over its trading decisions, and that includes risk sizing, transfer automation, redemption handling and recovery from API or system failures. These are your responsibility. Keep your contact details current so the platform can reach you.

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
| I cannot withdraw from the Bot Account | Withdrawal is disabled by design | Redemptions go through the pool (Section 5) |
| An API call timed out; was the order placed? | Asynchronous API | Query the order or position before retrying (Section 7) |
| I hit a position limit on BTC or ETH | Standard contract limits | Use BTCSPARTANS or ETHSPARTANS |
| No profit share this week | NAV did not exceed the HWM, or settlement has not run | See Section 8; weekly settlement is Monday UTC+0 |
| A redemption has waited a long time | Not enough Funding, or risk was too high to release funds | Follow the playbook (Section 5.6); aim for 5 days |

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

**Where is the API documentation?** In this repository: Open API V2 (https://raw.githubusercontent.com/Onebullex-dev/spartan-strategy-partner-skill/main/references/api/openapi-en.md, Chinese https://raw.githubusercontent.com/Onebullex-dev/spartan-strategy-partner-skill/main/references/api/openapi-zh.md) and the MCP guide (https://raw.githubusercontent.com/Onebullex-dev/spartan-strategy-partner-skill/main/references/api/mcp-en.md, Chinese https://raw.githubusercontent.com/Onebullex-dev/spartan-strategy-partner-skill/main/references/api/mcp-zh.md). Live version: https://doc.onebullex.com/#/

---

## 15. Change Timeline

| Date | Change |
|---|---|
| 29 Jul 2026 | Strategy provider profit-sharing tier mechanism takes effect |
| 18 Aug 2026 (announced) | Platform usage fee of 10% of the profit share payable, effective 1 Sep 2026. Profit generated up to 31 Aug 2026 is not charged. |
| 25 Aug 2026 | Profit share calculation moves to settlement on net value (weekly or monthly), with HWM |
| Latest tier table | Redemption-time requirement per tier; "strategy provider fee" and "platform fee" shown separately |

Always check the latest official announcement. If this guide and an announcement differ, the announcement prevails.

---

## 16. Glossary and Translation Notes

| Term | Definition |
|---|---|
| AUM | Capital currently allocated to your strategy |
| Bot Account | The dedicated, trade-only account created for your bot |
| Console | The strategy partner's management page (formerly the Apply button) |
| Funding wallet | Entry/exit wallet; cannot trade; not margin |
| Futures wallet | Trading wallet and margin |
| HWM | High-Water Mark: highest NAV per share that has already produced profit share |
| NAV | Net Asset Value per share |
| Open Window | Top of each hour: subscriptions processed, redemptions checked |
| Pending Redemption | Total redemption value waiting to be paid |
| Pool | Funding + Futures of the Bot Account |
| Principal capital | The Strategy Partner's own subscribed capital |
| Settlement account | Intermediate account in the subscription and redemption routing |
| Share | Proportional ownership of the pool |
| Strategy Partner | The person who runs the bot |

**For translators and AI assistants:** keep these terms in English or use the platform's own translation: Funding, Futures, NAV, HWM, Open Window, Pending Redemption, Bot Account, Strategy Partner, Console, Spartan/Spartans, and the tier names. The diagrams are plain text, so their labels can be translated directly.

*This guide explains how Spartan works as documented by the OneBullEx team. It is not investment advice. Historical returns do not guarantee future results. Operating your strategy, including risk sizing, automation and failure handling, is your own responsibility. See the Spartans Risk Disclosure for the full terms.*

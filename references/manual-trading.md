# For manual traders

> Generated from `docs/Spartan_Strategy_Partner_Guide.md` by `scripts/split_guide.py`. Edit the guide, not this file.

Contents: 6. For Manual Traders

---

## 6. For Manual Traders

If you trade through the Bot Account login, you run the pool by hand. Everything in Section 5 of `deposits-and-redemptions.md` applies to you, and you do these jobs yourself.

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

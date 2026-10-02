# Wallets, deposits and redemptions

> Generated from `docs/Spartan_Strategy_Partner_Guide.md` by `scripts/split_guide.py`. Edit the guide, not this file.

Contents: 5. Wallets, Deposits and Redemptions

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

Aim to clear every redemption within 5 days. If requests stay unprocessed for an extended period, the platform may take risk-management measures to protect participants, such as reducing positions, partially closing positions, or ending the trading cycle. Redemption processing time is also one of your 30-day tier metrics (Section 9 of `profit-share-and-tiers.md`).

---

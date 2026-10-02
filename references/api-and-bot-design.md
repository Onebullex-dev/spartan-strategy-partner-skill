# For API traders and bot builders

> Generated from `docs/Spartan_Strategy_Partner_Guide.md` by `scripts/split_guide.py`. Edit the guide, not this file.

Contents: 7. For API Traders and Bot Builders

---

## 7. For API Traders and Bot Builders

> **Your responsibility.** This section explains how the system behaves and what your design has to account for. How you size risk, automate transfers, handle redemptions and recover from API failures is your own design decision and your responsibility as a quant. OneBullEx does not provide a standard bot or sweeper, and nothing here guarantees that a particular design is safe.

### 7.1 What the API Gives You

The API covers trading, balances, positions and account transfers (reference: https://raw.githubusercontent.com/Onebullex-dev/spartan-strategy-partner-skill/main/references/api/openapi-en.md, Chinese: https://raw.githubusercontent.com/Onebullex-dev/spartan-strategy-partner-skill/main/references/api/openapi-zh.md; live version: https://doc.onebullex.com/#/). For MCP see https://raw.githubusercontent.com/Onebullex-dev/spartan-strategy-partner-skill/main/references/api/mcp-en.md. The redemption queue summary is available at `GET /v2/bot/redeeming-info` (no request parameters), so your code can see pending redemptions without relying on the Console or email. You can build whatever mechanism you prefer on top of it, for example an automatic redemption mode, an alert, or fully automated handling. The Console and email still work alongside it.

### 7.2 Bot Design Checklist

1. **Define your sizing base.** Decide whether you size from Futures equity or from the pool total (Funding + Futures). Platform NAV and ROI use the pool total. If you size from Futures only, keep idle Funding small or read both balances.
2. **Re-read equity before every new position.** The pool changes through deposits, redemptions and PnL. A fixed lot size or a fixed assumed balance will drift away from your intended risk.
3. **Treat redemptions as normal events.** Cap your open risk so that a plausible redemption-sized transfer out of Futures does not endanger your positions.
4. **Design the sweeper carefully.** Fixed minute of the hour, not continuous; pause it while clearing redemptions (Section 5.7 of `deposits-and-redemptions.md`).
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
15. **Test small.** Expect live results to differ from a backtest: deposits and redemptions change the pool while trades are open (Section 12 of `scenarios.md`).

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

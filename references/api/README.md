# API documentation

> STATUS: EMPTY. To be added by the maintainer.

Canonical source: https://doc.onebullex.com/#/ (always the live reference. If anything here conflicts with it, the live docs win.)

## How to add the docs

1. Copy the API documentation from the site and convert it to Markdown (any AI assistant can do this).
2. Save one file per area in this folder, for example `authentication.md`, `trading.md`, `positions-and-orders.md`, `account-transfer.md`, `bot-endpoints.md`.
3. Start every file with this header:

```text
# <Area name>
Source: <exact URL>
Snapshot date: <YYYY-MM-DD>
Live docs win if they conflict with this file.
```

4. Keep each file focused (about 500 lines at most). Do not paste API keys, secrets, UIDs or any personal data.
5. Add one line per file to the list below, so an assistant can find the right one quickly.
6. When an endpoint is added or changed, update the file and its snapshot date.

## Files

(none yet)

## Endpoints already documented in this skill

- `POST /v2/balance/transfer`: account transfer (Funding <-> Futures). See "Fund Account" in the live docs.
- `GET /v2/bot/redeeming-info`: redemption queue summary, no request parameters.

Response fields are not documented here yet. Do not guess them.

# API documentation

Canonical source: https://doc.onebullex.com/#/ (the live reference. If anything here conflicts with it, the live docs win.)

## Files

Each area has an English file and a Chinese file (`.zh.md`) with the same name.

| English | Chinese | Area |
|---|---|---|
| `01-introduction-and-authentication.md` | `01-introduction-and-authentication.zh.md` | Introduction and authentication |
| `02-rate-limits-and-errors.md` | `02-rate-limits-and-errors.zh.md` | Rate limits and error codes |
| `03-market-data.md` | `03-market-data.zh.md` | Market data |
| `04-account-and-fund-transfer.md` | `04-account-and-fund-transfer.zh.md` | Account, balances and fund transfer |
| `05-trading-orders-and-positions.md` | `05-trading-orders-and-positions.zh.md` | Trading: orders and positions |
| `06-spartan-bot-endpoints.md` | `06-spartan-bot-endpoints.zh.md` | Spartan bot endpoints (including the redemption queue) |
| `07-websocket-streams.md` | `07-websocket-streams.zh.md` | WebSocket streams (if available) |
| `08-code-examples.md` | `08-code-examples.zh.md` | Code examples |

If your documentation is organized differently, rename or delete files, keep the `NN-` prefix and the `.zh.md` pairing, and update this table.

## Rules for assistants

- **A file is empty if it still contains the line "PASTE THE".** Treat empty files as missing. Do not guess their contents.
- Read the **English** file by default. Read the `.zh.md` file when the user writes in Chinese or asks for the Chinese documentation. If only the Chinese file has content, use it and say so.
- Never invent endpoints, parameters, response fields, limits or error codes.

## How the maintainer adds content

1. Open the file on GitHub and click the pencil icon (Edit).
2. Paste the documentation below the marker line, delete the marker line, and set the snapshot date.
3. Commit. Do not paste API keys, secrets, UIDs or any personal data.
4. When an endpoint is added or changed, update the file and its snapshot date.

## Endpoints already documented in this skill

- `POST /v2/balance/transfer`: account transfer (Funding <-> Futures). See "Fund Account" in the live docs.
- `GET /v2/bot/redeeming-info`: redemption queue summary, no request parameters.

Response fields are not documented here yet. Do not guess them.

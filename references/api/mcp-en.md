# OneBullEx MCP guide, English

> Source: https://doc.onebullex.com/#/ (onebullex-mcp-en-v2). Snapshot 2026-10-02, text unchanged, reformatted as Markdown. If anything conflicts with the live docs, the live docs win.

## OneBullEx MCP Setup Guide

Let AI assistants (Claude Code, Codex, Cursor, etc.) call the OneBullEx perpetual-futures API directly: check market data, view balances, open/close positions, query trade history.

MCP (Model Context Protocol) is the standard protocol AI clients use to call external tools. Once OneBullEx MCP is installed, you only need to give natural-language instructions in chat — the AI will operate your account on your behalf.

## 1. Install

Requires Node.js ≥ 20.

```bash
# 1. Install the CLI (used to configure your API key)
npm i -g @onebullex-group/cli

# 2. Install the MCP server
npm i -g @onebullex-group/mcp
```

**Verify:**

```bash
onebullex --version
onebullex-mcp --help
```

Don't want a global install? Replace every onebullex-mcp below with npx -y @onebullex-group/mcp.

## 2. Configure your API key

Run the interactive wizard once. It writes the key/secret to ~/.onebullex/config.json in plaintext (mode 0600):

```bash
onebullex config init
```

**Fill in the prompts:**

| Field | Description |
|---|---|
| profile name | Pick your own, e.g. test or prod |
| env | test (testnet) or prod (production) |
| base-url | Testnet https://futures-openapi.1bullex.com; Production https://futures-openapi.onebullex.com |
| api-key | API Key generated in the OneBullEx dashboard |
| secret | The matching Secret |

**Verify connectivity:**

```bash
onebullex public time     # Public endpoint, no key needed
onebullex balance list    # Private endpoint, validates key + signature
```

Security note: API Key and Secret are stored in plaintext on disk. Do not commit ~/.onebullex/config.json to git, and never pass --api-key xxx on the command line (visible in ps and shell history).

## 3. Register the MCP server with your AI client

### Claude Code

**Use the official CLI command (do not hand-edit a config file):**

```bash
claude mcp add --scope user onebullex onebullex-mcp -- --profile test
```

**Arguments:**

- --scope user: available across all projects (alternatives: project / local)
- onebullex: name of the MCP server (your choice)
- onebullex-mcp: the executable to spawn
- --profile test: profile name from step 2

**Verify:**

```bash
claude mcp list
claude mcp get onebullex
```

Restart your Claude Code session and type /mcp. You should see onebullex connected with a non-empty tool list (at least including balance_list).

### Codex CLI

**Edit ~/.codex/config.toml:**

```toml
[mcp_servers.onebullex]
command = "onebullex-mcp"
args = ["--profile", "test"]
```

Start codex and the tools appear automatically.

### Cursor

**Drop .cursor/mcp.json at the repo root (or ~/.cursor/mcp.json for user-wide):**

```json
{
  "mcpServers": {
    "onebullex": {
      "command": "onebullex-mcp",
      "args": ["--profile", "test"]
    }
  }
}
```

Restart Cursor; the MCP indicator (bottom-left) should turn green.

### Claude Desktop

**Edit:**

- macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
- Windows: %APPDATA%\Claude\claude_desktop_config.json

```json
{
  "mcpServers": {
    "onebullex": {
      "command": "onebullex-mcp",
      "args": ["--profile", "test"]
    }
  }
}
```

Fully quit Claude Desktop (kill the process, not just close the window) and relaunch.

## 4. Usage examples

Just talk to the AI. It picks the right tool.

### Example 1 — Check balance

```text
Show my account balance.
```

The AI calls balance_list and returns available / frozen / total per asset.

**Variations:**

```text
How much USDT do I have available right now?
```

```text
Show the last 7 days of fund flows (deposits, fees, P&L).
```

The latter calls balance_bills.

### Example 2 — Open a position (limit long)

```text
Place a limit BUY order on BTC perpetuals to go long, price 50000, size 1 contract.
```

**Expected flow:**

First call (without confirm): the tool returns a dry-run preview showing the request body that would be sent:

```json
{
  "dryRun": true,
  "request": {
    "method": "POST",
    "path": "/v2/order/create",
    "body": {
      "symbol": "btc_usdt",
      "orderType": "LIMIT",
      "orderSide": "BUY",
      "positionSide": "LONG",
      "origQty": "1",
      "price": "50000"
    }
  },
  "message": "Pass confirm:true to execute. Review the body carefully before confirming."
}
```

The AI shows the preview and waits for you.

After you reply "confirm", the AI calls the tool again with confirm: true, and only then is the order actually placed.

Safety guardrail: every write tool (place/cancel order, change leverage, close position) is dry-run by default and requires the boolean confirm: true to execute. The string "true" is rejected. This is intentional — it prevents the AI from blowing up real money on a misread instruction.

Installing the companion @onebullex-group/skill plugin makes Claude Code follow the dry-run → user-confirm → execute discipline by convention. Other clients are still protected by the server-side guard, but it's worth eyeballing the preview yourself before you say "confirm".

origQty must be an integer number of contracts; fractional values are rejected by the server (invalid_quantity).

### Example 3 — Close a position

```text
Close all my BTC positions.
```

The AI calls position_close_all. Same dry-run → confirm flow as above.

**Partial close:**

```text
Reduce my BTC long by 50%.
```

The AI first calls position_list to read the current size, halves it, and submits a market order in the opposite direction.

### Example 4 — Query historical trade orders

```text
Show today's filled trades.
```

The AI calls order_trades and lists today's fills in reverse-chronological order (price, size, fee).

**By symbol:**

```text
Which BTC perp orders did I place this past week, and which got filled?
```

Combines order_list_history and order_trades into a P&L summary.

**Open orders:**

```text
What orders do I have open right now?
```

Calls order_list_unfinished.

## 5. Troubleshooting

| Symptom | Fix |
|---|---|
| onebullex-mcp: command not found | npm's global bin is not on PATH. Run npm config get prefix and add `<prefix>`/bin to PATH |
| Claude Code's /mcp doesn't list onebullex | You didn't run claude mcp add, or didn't restart the session. Confirm with claude mcp list |
| Tool returns api-key required | Profile not configured in step 2, or --profile name is wrong |
| Signature mismatch | System clock differs from server by more than ±30s — sync your clock |
| /mcp tool list is empty or missing balance_list | cli/mcp version mismatch or server failed to start. Run npm i -g @onebullex-group/cli@latest @onebullex-group/mcp@latest and restart the session |
| AI executed a write op without asking | Install @onebullex-group/skill: npm i -g @onebullex-group/skill to enforce the dry-run discipline |

## 6. Security recommendations

- Always start on testnet with prices far from market and tiny size. Validate the full flow before switching to production.
- Don't trust the AI's dry-run preview blindly. Read the body yourself before answering "confirm".
- Grant your API key only the permissions it needs in the OneBullEx dashboard (don't enable withdrawal if you don't need it).
- After a one-off task, revoke the key from the dashboard and rotate when needed.
- Done.

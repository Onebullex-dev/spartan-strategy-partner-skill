# Spartan Strategy Partner Skill

An operating guide for running a strategy (bot) on **OneBullEx Spartan**, a pooled strategy-trading system, packaged so that **people and AI assistants can both use it**. It explains the pool mechanics (Funding vs Futures wallets, shares and NAV), subscriptions and redemptions, profit sharing and tiers, the three account types, API and manual trading cautions, and worked scenarios and troubleshooting.

## Use it with an AI assistant (link only)

Give your assistant this repository link and this instruction:

> Read https://github.com/Onebullex-dev/spartan-strategy-partner-skill, starting with `SKILL.md`, and follow it whenever you help me with OneBullEx Spartan.

**For AI assistants:** start with [`SKILL.md`](SKILL.md). It holds the model, the hard rules, and a table saying which file to read for which task. Fetch only the files you need. Raw files are available at `https://raw.githubusercontent.com/Onebullex-dev/spartan-strategy-partner-skill/main/<path>`.

> The link works for an assistant only while the repository is **public**. A private repository cannot be read from a link.

## Repository layout

```text
SKILL.md                          entry point for AI assistants
README.md                         this file
references/
  overview.md                     model, wallets, NAV, account types
  setup-and-bot-console.md        onboarding, bot setup, Console, bot closure
  deposits-and-redemptions.md     deposits, redemption queue, sweeper rules
  manual-trading.md               manual trader workflow
  api-and-bot-design.md           bot design checklist, decisions that are yours
  profit-share-and-tiers.md       high-water mark, fees, tier table
  risk-and-pairs.md               Spartan pairs, limits, liquidation
  scenarios.md                    worked numeric scenarios
  troubleshooting-and-faq.md      symptoms and FAQ
  changelog-and-glossary.md       rule-change timeline, glossary, translation notes
  mcp.md                          MCP access (to be filled in)
  api/                            API documentation (to be filled in)
docs/
  Spartan_Strategy_Partner_Guide.md   the full guide for people (single source of truth)
scripts/
  split_guide.py                  regenerates references/ from the guide
```

## Install as a skill

- **Claude Code:** `git clone https://github.com/Onebullex-dev/spartan-strategy-partner-skill ~/.claude/skills/spartan-strategy-partner` (all projects), or clone into `<your-project>/.claude/skills/spartan-strategy-partner`.
- **Claude (web/desktop):** upload a zip of a folder named `spartan-strategy-partner` that contains `SKILL.md` and `references/`, in the Skills settings.
- **Other AI tools:** `SKILL.md` is plain Markdown. Paste it (plus the files you need) into the tool's rules or instructions, or give the assistant the link as above. Check the tool's documentation for its current mechanism.
- **People:** read `docs/Spartan_Strategy_Partner_Guide.md`.

## Adding the API documentation

In `references/api/`, add one Markdown file per area (for example `authentication.md`, `trading.md`, `account-transfer.md`). On GitHub: open the `references/api` folder, choose **Add file, Create new file**, type the file name, paste the content, and commit. Follow the header format in `references/api/README.md`. Fill in `references/mcp.md` the same way. Never paste API keys, secrets, UIDs or personal data.

## Updating the guide

1. Edit `docs/Spartan_Strategy_Partner_Guide.md` (never the generated files in `references/`).
2. Run `python scripts/split_guide.py` from the repository root.
3. Commit the guide and the regenerated files.

`references/api/` and `references/mcp.md` are maintained by hand.

## Status

- API and MCP documentation: to be added.
- Statements marked "currently" or "at the time of writing" can change. If this repository conflicts with an official OneBullEx announcement, the announcement prevails.

## Disclaimer

This repository explains how Spartan works as understood by its maintainers. It is operating guidance, not investment advice, and not a guarantee of any outcome. How you size risk, automate transfers, handle redemptions and recover from API or system failures is your own responsibility.

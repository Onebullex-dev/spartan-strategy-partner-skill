# Spartan Strategy Partner Skill

An operating guide for running a strategy (bot) on **OneBullEx Spartan**, a pooled strategy-trading system, packaged so that **people and AI assistants can both use it**. It explains the pool mechanics (Funding vs Futures wallets, shares and NAV), subscriptions and redemptions, profit sharing and tiers, the three account types, API and manual trading cautions, and worked scenarios and troubleshooting.

## Use it with an AI assistant

Copy this prompt into your AI assistant (it must be able to open web pages):

> Read https://github.com/Onebullex-dev/spartan-strategy-partner-skill, starting with `SKILL.md`. Before answering any question about OneBullEx Spartan, open the files that apply and follow them. Do not answer from memory.

If your assistant can open only one page, use this prompt instead:

> Read https://raw.githubusercontent.com/Onebullex-dev/spartan-strategy-partner-skill/main/docs/Spartan_Strategy_Partner_Guide.md and use it to answer my questions about OneBullEx Spartan.

An assistant without web access cannot read a link. In that case paste the contents of `SKILL.md` and the files you need, or install the skill (see below).

**For AI assistants:** start with [`SKILL.md`](SKILL.md). Open the files that apply before answering. An index of all files is in [`llms.txt`](llms.txt). Raw files are at `https://raw.githubusercontent.com/Onebullex-dev/spartan-strategy-partner-skill/main/<path>`.

## Repository layout

```text
SKILL.md                          entry point for AI assistants
llms.txt                          index of all files for AI assistants
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
  api/                            API documentation, English (NN-*.md) and Chinese (NN-*.zh.md)
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

The files are already created in `references/api/` (English `NN-*.md`, Chinese `NN-*.zh.md`). Open a file on GitHub, click the pencil icon, paste the documentation below the marker line, delete the marker line, and commit. See `references/api/README.md`. Fill in `references/mcp.md` the same way. Never paste API keys, secrets, UIDs or personal data.

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

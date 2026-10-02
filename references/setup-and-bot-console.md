# Setup, Bot Console and bot lifecycle

> Generated from `docs/Spartan_Strategy_Partner_Guide.md` by `scripts/split_guide.py`. Edit the guide, not this file.

Contents: 4. Getting Started and Bot Setup | 11. Bot Closure and Platform Rights

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

The Console shows pending redemptions live. They are also emailed to you, and your code can read the same queue summary from the API (Section 5.4 of `deposits-and-redemptions.md`).

### 4.5 Three Ways to Operate

| Method | How it works |
|---|---|
| **API** | Trade with your bot's API Key and Secret Key. Full documentation: https://doc.onebullex.com/#/ |
| **Manual** | Log into the Bot Account and trade as you would on a normal futures account. You see Funding and Futures in one place. |
| **MCP** | A protocol-based way to connect, effectively a form of API trading. Described in the API documentation. |

Account transfers (Funding <-> Futures) can be done through the API: `POST /v2/balance/transfer` (see the "Fund Account" section of the API documentation).

---

---

## 11. Bot Closure and Platform Rights

- **Closing a bot.** A bot is removed once it has been liquidated, meaning its positions are closed and its subscribers have been redeemed. To retire a bot on purpose, contact your BD or support. Do not simply stop trading, because subscribers remain in the pool.
- **Platform rights.** To protect participants' funds and system stability, the platform reserves the right to take measures where needed, for example restricting new subscriptions, pausing a bot, reducing or closing positions, liquidating the bot, or removing it from the platform. Typical triggers are redemptions left unprocessed for an extended period, serious rule violations, risk events, or being unable to reach the manager.
- **Responsibility.** You operate your strategy with full autonomy over its trading decisions, and that includes risk sizing, transfer automation, redemption handling and recovery from API or system failures. These are your responsibility. Keep your contact details current so the platform can reach you.

---

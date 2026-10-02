# OneBullEx MCP guide, Chinese

> Source: https://doc.onebullex.com/#/ (onebullex-mcp-cn-v2). Snapshot 2026-10-02, copied verbatim. If anything conflicts with the live docs, the live docs win.

OneBullEx MCP 使用指引
让 Claude Code、Codex、Cursor 等 AI 助手直接调用 OneBullEx 合约 API：查行情、看余额、开/平仓、查历史订单。

MCP（Model Context Protocol）是 AI 客户端调用外部工具的标准协议。装上 OneBullEx MCP 后，你只需要在对话里用自然语言下指令，AI 就能帮你操作账户。

一、安装
需要 Node.js ≥ 20。

# 1. 装 CLI（用来配置 API Key）
npm i -g @onebullex-group/cli

# 2. 装 MCP server
npm i -g @onebullex-group/mcp
Copy to clipboardErrorCopied
校验：

onebullex --version
onebullex-mcp --help
Copy to clipboardErrorCopied
不想全局安装也行：所有 onebullex-mcp 命令换成 npx -y @onebullex-group/mcp 即可。

二、配置 API Key
跑一次交互式向导，会把 key/secret 明文存到 ~/.onebullex/config.json（权限 0600）：

onebullex config init
Copy to clipboardErrorCopied
按提示填：

字段	说明
profile name	自己起，比如 test 或 prod
env	test（测试网）或 prod（生产）
base-url	测试网 https://futures-openapi.1bullex.com；生产 https://futures-openapi.onebullex.com
api-key	OneBullEx 后台生成的 API Key
secret	配套的 Secret
验证联通性：

onebullex public time     # 公开接口，不需要 key
onebullex balance list    # 私有接口，验证签名/key 通了
Copy to clipboardErrorCopied
安全提示：API Key 和 Secret 明文落盘。请勿把 ~/.onebullex/config.json 提交到 git，也不要在命令行里以 --api-key xxx 方式传（会被 ps / shell history 看到）。

三、注册到 AI 客户端
Claude Code
用官方 CLI 命令注册（不要手写配置文件）：

claude mcp add --scope user onebullex onebullex-mcp -- --profile test
Copy to clipboardErrorCopied
参数：

--scope user：所有项目都能用（也可改 project / local）
onebullex：MCP server 名（自取）
onebullex-mcp：要执行的命令
--profile test：用第二步配置的 profile 名
验证：

claude mcp list
claude mcp get onebullex
Copy to clipboardErrorCopied
重启 Claude Code 会话，输入 /mcp 应该能看到 onebullex 状态 connected，且工具列表非空（至少包含 balance_list）。

Codex CLI
编辑 ~/.codex/config.toml：

[mcp_servers.onebullex]
command = "onebullex-mcp"
args = ["--profile", "test"]
Copy to clipboardErrorCopied
启动 codex，工具自动出现在工具列表。

Cursor
仓库根放 .cursor/mcp.json 或 ~/.cursor/mcp.json：

{
  "mcpServers": {
    "onebullex": {
      "command": "onebullex-mcp",
      "args": ["--profile", "test"]
    }
  }
}
Copy to clipboardErrorCopied
重启 Cursor，左下角 MCP 状态灯变绿即生效。

Claude Desktop
编辑：

macOS：~/Library/Application Support/Claude/claude_desktop_config.json
Windows：%APPDATA%\Claude\claude_desktop_config.json
{
  "mcpServers": {
    "onebullex": {
      "command": "onebullex-mcp",
      "args": ["--profile", "test"]
    }
  }
}
Copy to clipboardErrorCopied
完全退出 Claude Desktop（不是关窗口，是退出进程）再打开。

四、使用示例
直接用自然语言对 AI 说话，它会自己选合适的工具调用。

示例 1：查询余额
看下我账户余额。
Copy to clipboardErrorCopied
AI 会调 balance_list，返回每个币种的可用 / 冻结 / 总额。

进阶：

我现在 USDT 还有多少可用？
Copy to clipboardErrorCopied
查一下最近 7 天的资金流水（充值、手续费、盈亏）。
Copy to clipboardErrorCopied
后者会调 balance_bills。

示例 2：开仓（限价单做多）
帮我在 BTC 永续合约上挂一个限价 BUY 单做多，价格 50000，数量 1 张。
Copy to clipboardErrorCopied
AI 应该按以下流程：

第一次调用（不带 confirm）：返回 dry-run 预览，把要发的请求体展示给你

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
Copy to clipboardErrorCopied
AI 把这个预览给你看，等你确认。

你回 "确认" 后，AI 才会重新调一次工具，这次带 confirm: true，真正下单。

安全护栏：所有写操作（下单/撤单/改杠杆/平仓）默认是 dry-run，必须传布尔 confirm: true 才真发请求。字符串 "true" 不接受。这是故意的，防止 AI 误操作把真钱亏掉。

配套安装 @onebullex-group/skill 插件后，Claude Code 会按规范走 dry-run → 用户确认 → 真下单 流程；其他客户端也受 server 端护栏保护，但建议人工盯一眼预览再答 "确认"。

origQty 必须为整数张数；带小数位会被服务端拒绝（invalid_quantity）。

示例 3：平仓
把我手上 BTC 的所有持仓全部平掉。
Copy to clipboardErrorCopied
AI 会调 position_close_all，同样会先 dry-run 给你看，确认后才执行。

只想平一部分：

帮我减 50% 的 BTC 多仓。
Copy to clipboardErrorCopied
AI 会先 position_list 查当前持仓数量，再算出 0.5 倍仓位，发市价反向单平掉。

示例 4：查询历史成交订单
查一下我今天的所有成交记录。
Copy to clipboardErrorCopied
AI 会调 order_trades，按时间倒序列出今天的所有成交（含成交价、数量、手续费）。

按交易对筛选：

最近一周 BTC 永续我下了哪些单？成交了哪些？
Copy to clipboardErrorCopied
会组合调用 order_list_history + order_trades，给你一份盈亏汇总。

未成交的挂单：

我现在有哪些挂着没成交的订单？
Copy to clipboardErrorCopied
调 order_list_unfinished。

五、常见问题
现象	解法
onebullex-mcp: command not found	npm 全局 bin 不在 PATH，跑 npm config get prefix 加进去
Claude Code 里 /mcp 看不到 onebullex	没用 claude mcp add 注册，或注册了没重启会话；用 claude mcp list 确认
工具调用返回 api-key required	第二步没配 profile，或 --profile 名字打错
返回 Signature mismatch	本机时间和服务器偏差超过 ±30 秒，校准系统时间
/mcp 工具列表为空或不含 balance_list	cli / mcp 版本不匹配或未正确启动，跑 npm i -g @onebullex-group/cli@latest @onebullex-group/mcp@latest 后重启会话
AI 没经确认就下单	装上 @onebullex-group/skill：npm i -g @onebullex-group/skill，让 AI 按 dry-run 纪律走
六、安全建议
第一次跑务必用测试网 + 远离市场价 + 小额，把流程走通再切生产
写操作不要盲目相信 AI 的 dry-run 预览，自己看一眼 body 再答 "确认"
API Key 在 OneBullEx 后台只开必要权限（不需要提币就别勾提币）
用完一次性会话后，可在后台把 key 注销，下次再生成新的
完。


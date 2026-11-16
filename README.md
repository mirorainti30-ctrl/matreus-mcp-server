# Matreus Risk & Regime Oracle (MCP Server & REST API)

**A quantitative trading guardrail and out-of-sample Walk-Forward validation engine for AI agents (Claude Desktop, Cursor, LangChain, and custom bots).**

Large Language Models are great at reasoning, but they are notoriously overconfident when executing financial trades—often ignoring transaction costs, historical drawdowns, and statistical overfitting. **Matreus Risk & Regime Oracle** acts as a strict, data-driven veto layer that checks whether an asset actually has a proven statistical edge before your AI agent risks capital.

Live Dashboard & Docs: **[https://www.matreus.com](https://www.matreus.com)**

---

## Key Features

- **Strict Walk-Forward Quality Gate:** Evaluates US equities, ETFs, European stocks, and crypto across multi-year out-of-sample windows—automatically rejecting negative-edge or high-drawdown assets.
- **Cognitive WorldModel Memory:** Adjusts asset confidence dynamically based on live trade feedback and regime shifts.
- **Exact Position Sizing:** Calculates maximum safe USD position sizes based on your account equity, max risk per trade, and the asset's historical maximum drawdown.
- **Millisecond Latency:** Pre-computed nightly batch validation combined with real-time memory lookups.

---

## Quick Start (MCP for Claude Desktop & Cursor)

### 1. Get a Free API Key
Generate an instant **Free Tier API key (14 requests/month)** directly on the homepage at **[https://www.matreus.com](https://www.matreus.com)**. *(Unlimited Pro access is available for \$19/mo).*

### 2. Clone & Install Dependencies
```bash
git clone https://github.com/mirorainti30-ctrl/matreus-mcp-server.git
cd matreus-mcp-server
pip install -r requirements.txt
```

### 3. Add to Claude Desktop (`claude_desktop_config.json`)
Add the following configuration to your Claude Desktop config file:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "matreus-risk-oracle": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/matreus-mcp-server/mcp_client.py"],
      "env": {
        "MATREUS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```
*(Note: On Windows, replace `"python"` with `"py"` and add `"-3.12"` as the first item in `"args"` if needed).*

---

## Available MCP Tool

### `evaluate_trade_risk`
Validates a trade setup before execution.

**Parameters:**
- `ticker` *(string, required)*: Asset ticker symbol (e.g., `"AAPL"`, `"SOXL"`, `"NVDA"`, `"BTC/USD"`).
- `direction` *(string, optional)*: `"LONG"` (daily swing, default) or `"FAST"` (15m intraday).
- `account_size` *(float, optional)*: Total portfolio size in USD (default: `10000.0`).
- `max_risk_per_trade_pct` *(float, optional)*: Maximum allowed risk per trade in % (default: `1.0`).

**Example Output:**
```text
Decision: APPROVED (Confidence: 76%)
Reasoning: APPROVED (LONG SOXL): 40 out-of-sample trades, net return +276.84%, win rate 65.0%.
Out-of-Sample Win Rate: 65.0% | Max Drawdown: -56.01%
Recommended Position Size: \$178.54
```

---

## Direct REST API Usage

You can also query the engine directly from any Python script or custom trading bot without MCP. Interactive Swagger documentation is available at **[https://www.matreus.com/docs](https://www.matreus.com/docs)**.

```bash
curl -X POST "https://www.matreus.com/v1/evaluate-trade" \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "direction": "LONG",
    "account_size": 10000,
    "max_risk_per_trade_pct": 1.0
  }'
```

---

## Disclaimer
*Matreus Risk & Regime Oracle provides quantitative statistical metrics and risk-sizing calculations for informational and algorithmic decision-support purposes only. It does not constitute financial advice. Algorithmic trading carries substantial risk of loss.*

import os
import httpx

try:
    from mcp.server.mcpserver import MCPServer
except ImportError:
    from mcp.server.fastmcp import FastMCP as MCPServer

mcp = MCPServer("Matreus Risk Oracle")

API_URL = os.environ.get("MATREUS_API_URL", "https://www.matreus.com/v1/evaluate-trade")
API_KEY = os.environ.get("MATREUS_API_KEY", "")


@mcp.tool()
def evaluate_trade_risk(
    ticker: str,
    direction: str = "LONG",
    account_size: float = 10000.0,
    max_risk_per_trade_pct: float = 1.0
) -> str:
    """
    Validates the out-of-sample statistical edge, win rate, historical max drawdown,
    and safe position size for a stock, ETF, or crypto asset before opening a trade.
    Always call this guardrail tool before executing a trade.
    """
    if not API_KEY:
        return (
            "Configuration Error: MATREUS_API_KEY environment variable is missing. "
            "Get a free API key (14 requests/month) at https://www.matreus.com"
        )

    headers = {"X-API-Key": API_KEY}
    payload = {
        "ticker": ticker.upper().strip(),
        "direction": direction.upper().strip(),
        "account_size": account_size,
        "max_risk_per_trade_pct": max_risk_per_trade_pct
    }

    try:
        response = httpx.post(API_URL, json=payload, headers=headers, timeout=10.0)
        if response.status_code == 401:
            return "Authentication Error: Invalid MATREUS_API_KEY."
        if response.status_code == 429:
            return "Rate Limit Reached: Monthly Free tier limit (14 calls) exceeded. Upgrade to Pro at https://www.matreus.com"
        response.raise_for_status()
        data = response.json()

        decision = "APPROVED" if data["approved"] else "VETOED (BLOCKED)"
        return (
            f"Decision: {decision} (Confidence: {data['confidence_score']:.0%})\n"
            f"Reasoning: {data['reason']}\n"
            f"Out-of-Sample Win Rate: {data['win_rate_pct']}% | Max Drawdown: {data['max_drawdown_pct']}%\n"
            f"Recommended Position Size: ${data['recommended_position_usd']}"
        )
    except Exception as e:
        return f"Connection error to Matreus Risk Oracle: {str(e)}"


if __name__ == "__main__":
    mcp.run()

import streamlit as st
import pandas as pd
import yfinance as yf

# -------------------------------
# TEMPORARY: Hardcoded API KEYS
# -------------------------------
TRADING_ECON_API_USER = "c88d1d122399451"
TRADING_ECON_API_PASS = "rdog9czpshn7zb9"
FINNHUB_API_KEY = "d1uv2rhr01qujmdeohv0d1uv2rhr01qujmdeohvg"

# -------------------------------
# STOCKS LIST (NASDAQ-100)
# -------------------------------
stock_list = [
    "NVDA", "MSFT", "AAPL", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "AVGO", "COST", "AMD", "NFLX",
    "ABNB", "ADBE", "ADI", "ADP", "ADSK", "AEP", "AMAT", "AMGN", "APP", "ANSS", "ARM", "ASML", "AXON",
    "AZN", "BIIB", "BKNG", "BKR", "CCEP", "CDNS", "CDW", "CEG", "CHTR", "CMCSA", "CPRT", "CSGP", "CSCO",
    "CSX", "CTAS", "CTSH", "CRWD", "DASH", "DDOG", "DXCM", "EA", "EXC", "FAST", "FANG", "FTNT", "GEHC",
    "GILD", "GFS", "HON", "IDXX", "INTC", "INTU", "ISRG", "KDP", "KHC", "KLAC", "LIN", "LRCX", "LULU",
    "MAR", "MCHP", "MDLZ", "MELI", "MNST", "MRVL", "MSTR", "MU", "NXPI", "ODFL", "ON", "ORLY", "PANW",
    "PAYX", "PYPL", "PDD", "PEP", "PLTR", "QCOM", "REGN", "ROP", "ROST", "SHOP", "SBUX", "SNPS", "TTWO",
    "TMUS", "TXN", "TTD", "VRSK", "VRTX", "WBD", "WDAY", "XEL", "ZS"
]

# -------------------------------
# Sidebar Controls
# -------------------------------
st.sidebar.title("📊 Scanner Settings")
timeframe = st.sidebar.selectbox("Select Timeframe", ["1m", "5m", "15m", "1h", "1d", "1wk", "1mo"])

# -------------------------------
# App Title
# -------------------------------
st.title("🧠 Multi-Sentiment Stock Scanner")

# -------------------------------
# Sentiment Score Logic (placeholder)
# -------------------------------
def get_combined_score(symbol):
    score = 0
    # Placeholder values — connect with real APIs later
    score += 1  # COT
    score += 1  # Earnings
    score += 1  # News
    score += 1  # Options
    score += 1  # Macro
    score += 1  # Geopolitical
    score += 1  # IPO
    return score

# -------------------------------
# Scan Stocks
# -------------------------------
results = []

for symbol in stock_list:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="5d", interval=timeframe)
        info = ticker.info

        price = data["Close"][-1] if not data.empty else None
        volume = data["Volume"][-1] if not data.empty else None
        float_shares = info.get("floatShares", 0)

        score = get_combined_score(symbol)
        sentiment = (
            "🟢 Bullish" if score > 0 else
            "🔴 Bearish" if score < 0 else
            "⚪ Neutral"
        )

        results.append({
            "Symbol": symbol,
            "Price": f"${price:.2f}" if price else "N/A",
            "Volume": f"{volume / 1e6:.2f}M" if volume else "N/A",
            "Float": f"{float_shares / 1e6:.2f}M" if float_shares else "N/A",
            "Score": f"+{score}" if score > 0 else f"{score}",
            "Sentiment": sentiment
        })

    except Exception as e:
        results.append({
            "Symbol": symbol,
            "Price": "Error",
            "Volume": "Error",
            "Float": "Error",
            "Score": "Error",
            "Sentiment": "❌"
        })

# -------------------------------
# Display Table
# -------------------------------
df = pd.DataFrame(results)
df = df.sort_values(by="Score", ascending=False)
st.dataframe(df, use_container_width=True)

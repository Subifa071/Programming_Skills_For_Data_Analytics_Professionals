# import yfinance as yf

# data = yf.download (['NVDA','AAPL','MSFT','AMZN','GOOGL','AVGO','GOOG','META','TSLA','BRK-B'], period = "10y", interval="1d")
# print(data,'DATATA')
import pandas as pd
import numpy as np
import yfinance as yf

# ============================================================
# CONFIG (easy to edit)
# ============================================================

# Your chosen 10 companies (all are in the S&P 500)
TICKERS = ['NVDA','AAPL','MSFT','AMZN','GOOGL','AVGO','GOOG','META','TSLA','BRK-B']

# Assignment requirements
PERIOD = "10y"        # last 10 years
INTERVAL = "1d"       # daily data
FORWARD_DAYS = 50     # hold period (50 days)

# SMA periods to test (you can change these)
SMA_PERIODS = list(range(10, 201, 5))  # 10..200 step 5


# ============================================================
# 1) Download Yahoo Finance data (10 years daily)
# ============================================================
# yfinance returns a DataFrame with multi-level columns when you download multiple tickers.
# Example: data["Close"]["AAPL"] gives AAPL close series.
data = yf.download(
    TICKERS,
    period=PERIOD,
    interval=INTERVAL,
    progress=False
)

# Basic validation (good practice)
if data.empty:
    raise RuntimeError("No data was downloaded. Check internet or ticker symbols.")

# Extract Close prices only (we only need Close for SMA and returns)
close_df = data["Close"].dropna(how="all")


# ============================================================
# 2) Function: find the best SMA period for a single stock
# ============================================================
def best_sma_for_stock(close: pd.Series, sma_periods, forward_days=50):
    """
    For one stock:
    - For each SMA period p:
        * Compute SMA(p)
        * Signal day = Close > SMA(p)   (assignment requirement)
        * Compute forward return for 50 days:
              forward_return[t] = Close[t+50] / Close[t] - 1
        * Score this SMA period by average forward return on signal days
    - Return the SMA period with the highest score.
    """
    close = close.dropna()

    # Need enough data for the largest SMA plus the forward holding period
    if len(close) < max(sma_periods) + forward_days + 5:
        return None

    # Forward 50-day return series aligned to today (t)
    forward_ret = close.shift(-forward_days) / close - 1

    best_period = None
    best_avg = -np.inf
    best_signals = 0

    # Test each SMA window length
    for p in sma_periods:
        sma = close.rolling(window=p, min_periods=p).mean()

        # Signal days: Close > SMA (as stated in the assignment)
        signal = close > sma

        # Only keep days where signal is true and forward return is known
        r = forward_ret[signal & forward_ret.notna()]

        if r.empty:
            continue

        avg_return = float(r.mean())

        # Keep the SMA period with the highest average forward return
        if avg_return > best_avg:
            best_avg = avg_return
            best_period = int(p)
            best_signals = int(len(r))

    if best_period is None:
        return None

    return {
        "Best_SMA": best_period,
        "Best_Avg_Forward_50d": best_avg,
        "Signals": best_signals
    }


# ============================================================
# 3) Compute best SMA for each of your 10 stocks
# ============================================================
results = []

for ticker in TICKERS:
    close = close_df[ticker].dropna()

    res = best_sma_for_stock(close, SMA_PERIODS, forward_days=FORWARD_DAYS)
    if res is None:
        # If a stock doesn't have enough valid data, skip it
        continue

    results.append({"Ticker": ticker, **res})

results_df = pd.DataFrame(results).dropna()

if results_df.empty:
    raise RuntimeError("No results were produced. Possibly insufficient data for all tickers.")


# ============================================================
# 4) Enforce "same SMA period" for the portfolio of 10
# ============================================================
# Since YOU fixed the portfolio to exactly these 10 stocks,
# the best way to meet the "same SMA period" condition is:
#
# - Evaluate each SMA period across all 10 stocks,
# - Compute the portfolio score (mean of the 10 average forward returns),
# - Choose the SMA period that maximises portfolio return.

portfolio_scores = []

for p in SMA_PERIODS:
    per_stock_returns = []

    for ticker in TICKERS:
        if ticker not in close_df.columns:
            continue

        close = close_df[ticker].dropna()

        # Need enough data for this SMA + forward period
        if len(close) < p + FORWARD_DAYS + 5:
            continue

        sma = close.rolling(window=p, min_periods=p).mean()
        signal = close > sma
        forward_ret = close.shift(-FORWARD_DAYS) / close - 1

        r = forward_ret[signal & forward_ret.notna()]
        if r.empty:
            continue

        per_stock_returns.append(float(r.mean()))

    # Only accept SMA periods that work for ALL 10 stocks (strict interpretation)
    if len(per_stock_returns) == len(TICKERS):
        portfolio_scores.append({
            "SMA_Period": p,
            "PortfolioMeanReturn": float(np.mean(per_stock_returns))
        })

portfolio_scores_df = pd.DataFrame(portfolio_scores).sort_values(
    "PortfolioMeanReturn", ascending=False
)

if portfolio_scores_df.empty:
    print("⚠️ No SMA period worked for all 10 stocks. Relax the strict condition if needed.")
else:
    chosen_sma_period = int(portfolio_scores_df.iloc[0]["SMA_Period"])
    print(f"\nChosen common SMA period for the portfolio: {chosen_sma_period} days\n")


# ============================================================
# 5) Outputs for evidence (CSV files)
# ============================================================
# Output 1: each stock’s best SMA period and score
results_df.to_csv("best_sma_per_stock.csv", index=False)

# Output 2: portfolio SMA scoring table (shows how common SMA was chosen)
portfolio_scores_df.to_csv("portfolio_sma_scores.csv", index=False)

print("Saved output files:")
print("- best_sma_per_stock.csv")
print("- portfolio_sma_scores.csv")

print("\nBest SMA for each stock (per-stock optimisation):\n")
print(results_df.to_string(index=False))

if not portfolio_scores_df.empty:
    print("\nTop SMA periods for the whole 10-stock portfolio:\n")
    print(portfolio_scores_df.head(10).to_string(index=False))

import pandas as pd
import numpy as np
import yfinance as yf # Yahoo Finance API wrapper to fetch historical market data

# List of 10 companies from the S&P 500 companies
TICKERS = ['NVDA','AAPL','MSFT','AMZN','GOOGL','AVGO','GOOG','META','TSLA','BRK-B']

PERIOD = "10y"        # Fetch last 10 years data
INTERVAL = "1d"       # Use daily frequency data
FORWARD_DAYS = 50     # Holding period for return calculation: 50 days 

# SMA periods to test (simple moving averages only)
SMA_PERIODS = list(range(10, 201, 5))  # from 10 to 200 days in steps of 5

# Download Yahoo Finance data (10 years daily)
data = yf.download(
    TICKERS,
    period=PERIOD,
    interval=INTERVAL,
    progress=False # Disable progress bar during download
) 

# If no data is returned, raise an error early
if data.empty:
    raise RuntimeError("No data was downloaded. Check internet or ticker symbols.")

# Extract only the closing prices (Close) for all tickers
close_df = data["Close"].dropna(how="all") # Drop rows where all ticker prices are NaN

# Find the best SMA period for a single stock
def best_sma_for_stock(close: pd.Series, sma_periods, forward_days=50):
    """
    Identifies the SMA period that gives the best average forward return
    for a given stock over a defined holding period (default: 50 days).

    The process:
    - For each SMA period:
        * Compute the simple moving average (SMA)
        * Generate buy signals when Close > SMA
        * Compute 50-day forward returns on those signal days
        * Score the SMA by averaging forward returns on signal days
    - Return the SMA period with the highest average forward return
    """

    close = close.dropna() # Remove NaNs to ensure valid calculations

    # Skip if not enough data for longest SMA + forward period
    if len(close) < max(sma_periods) + forward_days + 5:
        return None

    # Calculate forward return: (price 50 days ahead / current price) - 1
    forward_ret = close.shift(-forward_days) / close - 1

    best_period = None
    best_avg = -np.inf # Initialize with lowest possible return
    best_signals = 0

    # Loop through each SMA period candidate
    for p in sma_periods:
        # Compute SMA with minimum required data for each window
        sma = close.rolling(window=p, min_periods=p).mean()

        # Signal condition: current price is above SMA (Close > SMA)
        signal = close > sma

        # Only keep days where signal is true and forward return is known
        r = forward_ret[signal & forward_ret.notna()]

        if r.empty:
            continue # Skip if no valid signals

        avg_return = float(r.mean()) # Average return for this SMA

        # Keep the SMA period with the highest average forward return
        if avg_return > best_avg:
            best_avg = avg_return
            best_period = int(p)
            best_signals = int(len(r))

    if best_period is None:
        return None # No suitable SMA found

    return {
        "Best_SMA": best_period,
        "Best_Avg_Forward_50d": best_avg,
        "Signals": best_signals
    }

# Compute best SMA for each of your 10 stocks
# Run the above function for each stock and collect results
results = []

for ticker in TICKERS:
    close = close_df[ticker].dropna()

    res = best_sma_for_stock(close, SMA_PERIODS, forward_days=FORWARD_DAYS)
    if res is None:
        # If a stock doesn't have enough valid data, skip it
        continue

    results.append({"Ticker": ticker, **res}) # Merge ticker with its SMA results

# Convert results into a DataFrame for easier analysis/output
results_df = pd.DataFrame(results).dropna()

# If none of the stocks yielded results, raise an error
if results_df.empty:
    raise RuntimeError("No results were produced. Possibly insufficient data for all tickers.")

# Round average forward return to 4 decimal places for readability
results_df["Best_Avg_Forward_50d"] = results_df["Best_Avg_Forward_50d"].round(4)

"""
Enforce "same SMA period" for the portfolio of 10
    - Evaluate each SMA period across all 10 stocks,
    - Compute the portfolio score (mean of the 10 average forward returns),
    - Choose the SMA period that maximises portfolio return.
"""

portfolio_scores = []

for p in SMA_PERIODS:
    per_stock_returns = []

    for ticker in TICKERS:
        if ticker not in close_df.columns:
            continue

        close = close_df[ticker].dropna()

        # Ensure enough data for this SMA + forward period
        if len(close) < p + FORWARD_DAYS + 5:
            continue

        # Calculate SMA and signal as before
        sma = close.rolling(window=p, min_periods=p).mean()
        signal = close > sma
        forward_ret = close.shift(-FORWARD_DAYS) / close - 1

        # Filter valid signal days with known forward returns
        r = forward_ret[signal & forward_ret.notna()]
        if r.empty:
            continue

        per_stock_returns.append(float(r.mean()))

    # Only accept SMA periods that work for ALL 10 stocks 
    if len(per_stock_returns) == len(TICKERS):
        portfolio_scores.append({
            "SMA_Period": p,
            "PortfolioMeanReturn": float(np.mean(per_stock_returns))
        })

# Create DataFrame from portfolio-level SMA scores and sort descending by return
portfolio_scores_df = pd.DataFrame(portfolio_scores).sort_values(
    "PortfolioMeanReturn", ascending=False
)

if portfolio_scores_df.empty:
    print("No SMA period worked for all 10 stocks. Relax the strict condition if needed.")
else:
    # Select the top-performing SMA period for the portfolio
    chosen_sma_period = int(portfolio_scores_df.iloc[0]["SMA_Period"])
    print(f"\nChosen common SMA period for the portfolio: {chosen_sma_period} days\n")

# Round portfolio return values 
portfolio_scores_df["PortfolioMeanReturn"] = portfolio_scores_df["PortfolioMeanReturn"].round(4)

# ----- Outputs (CSV files) -----

# Output 1: each stock’s best SMA period and score
results_df.to_csv("best_sma_per_stock_static.csv", index=False)

# Output 2: portfolio SMA scoring table (shows how common SMA was chosen)
portfolio_scores_df.to_csv("portfolio_sma_scores_static.csv", index=False)

print("Saved output files:")
print("best_sma_per_stock_static.csv")
print("portfolio_sma_scores_static.csv")

print("\nBest SMA for each stock (per stock optimisation):\n")
print(results_df.to_string(index=False))

if not portfolio_scores_df.empty:
    print("\nTop SMA periods for the whole 10 stock portfolio:\n")
    print(portfolio_scores_df.head(10).to_string(index=False))
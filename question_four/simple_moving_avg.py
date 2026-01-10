import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import time
import requests
from bs4 import BeautifulSoup
from io import StringIO
from tqdm import tqdm

def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(url, headers=headers, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    df = pd.read_html(StringIO(str(table)))[0]
    return df["Symbol"].str.replace(".", "-", regex=False).tolist()

def download_close(ticker: str, start, end, max_retries=3, base_sleep=2.0):
    for attempt in range(1, max_retries + 1):
        try:
            df = yf.download(
                ticker,
                start=start,
                end=end,
                interval="1d",
                auto_adjust=False,
                progress=False,
                threads=False,
            )
            if df is None or df.empty:
                return None

            # Robust to MultiIndex columns
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            if "Close" not in df.columns:
                return None

            close = df["Close"].dropna()
            return close

        except Exception:
            if attempt == max_retries:
                return None
            time.sleep(base_sleep * attempt)
    return None

def best_sma_for_stock(close: pd.Series, sma_periods, forward_days=50):
    close = close.dropna()

    # Need enough history for biggest SMA + forward hold
    if len(close) < (max(sma_periods) + forward_days + 5):
        return None

    forward_ret = close.shift(-forward_days) / close - 1

    best_period = None
    best_avg = -np.inf
    best_n = 0

    for p in sma_periods:
        sma = close.rolling(window=p, min_periods=p).mean()
        signal = close > sma
        r = forward_ret[signal & forward_ret.notna()]
        if r.empty:
            continue
        avg = r.mean()
        if avg > best_avg:
            best_avg = float(avg)
            best_period = int(p)
            best_n = int(r.shape[0])

    if best_period is None:
        return None

    return {"Best_SMA": best_period, "Best_Avg_Forward_50d": best_avg, "Signals": best_n}

def main():
    tickers = get_sp500_tickers()
    end_date = dt.datetime.today()
    start_date = end_date - dt.timedelta(days=365 * 10)

    forward_days = 50
    sma_periods = list(range(10, 201, 5))  # 10..200 step 5 (edit if you want)

    rows = []
    for t in tqdm(tickers, desc="Downloading & scanning"):
        time.sleep(1.0)  # helps avoid throttling for big runs
        close = download_close(t, start_date, end_date)
        if close is None:
            continue

        res = best_sma_for_stock(close, sma_periods, forward_days=forward_days)
        if res is None:
            continue

        rows.append({"Ticker": t, **res})

    df = pd.DataFrame(rows).dropna()
    if df.empty:
        print("No results produced. Likely rate limiting / download failures.")
        return

    # Find SMA periods with at least 10 stocks
    counts = df.groupby("Best_SMA")["Ticker"].size().rename("Count").reset_index()
    eligible = counts[counts["Count"] >= 10].copy()
    if eligible.empty:
        print("No SMA period had >= 10 tickers with that as their best SMA.")
        print("Try widening sma_periods or lowering the >=10 requirement for debugging.")
        return

    # Choose the SMA period whose group has the highest mean return
    period_scores = (
        df.groupby("Best_SMA")["Best_Avg_Forward_50d"]
          .mean()
          .rename("MeanReturn")
          .reset_index()
          .merge(eligible, on="Best_SMA")
          .sort_values("MeanReturn", ascending=False)
    )
    chosen_period = int(period_scores.iloc[0]["Best_SMA"])

    top10 = (
        df[df["Best_SMA"] == chosen_period]
          .sort_values("Best_Avg_Forward_50d", ascending=False)
          .head(10)
          .reset_index(drop=True)
    )

    print(f"\nChosen common SMA period: {chosen_period} days")
    print("\nTop 10 stocks (same SMA period):\n")
    print(top10.to_string(index=False))

    top10.to_csv("top_10_sma_strategy.csv", index=False)
    period_scores.to_csv("sma_period_scores.csv", index=False)
    print("\nSaved: top_10_sma_strategy.csv and sma_period_scores.csv")

if __name__ == "__main__":
    main()

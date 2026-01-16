import pytest
import pandas as pd
import numpy as np
from question_four.simple_moving_avg import best_sma_for_stock

# Helper to create synthetic price data
def generate_price_series(length, start=100, drift=0.1, noise=1.0, seed=None):
    if seed:
        np.random.seed(seed)
    returns = np.random.normal(loc=drift, scale=noise, size=length)
    prices = start + np.cumsum(returns)
    return pd.Series(prices)

# Test: Valid case with strong signals
def test_best_sma_for_stock_valid_case():
    price_series = generate_price_series(300, seed=42)
    sma_periods = list(range(10, 51, 10))
    result = best_sma_for_stock(price_series, sma_periods, forward_days=50)

    assert result is not None
    assert "Best_SMA" in result
    assert "Best_Avg_Forward_50d" in result
    assert "Signals" in result
    assert isinstance(result["Best_SMA"], int)
    assert isinstance(result["Best_Avg_Forward_50d"], float)
    assert result["Signals"] > 0

# Test: Not enough data to compute SMA + forward return
def test_best_sma_for_stock_insufficient_data():
    price_series = generate_price_series(30)  # too short for SMA + 50d forward
    sma_periods = [10, 20]
    result = best_sma_for_stock(price_series, sma_periods, forward_days=50)
    assert result is None

# Test: SMA returns no valid signal days
def test_best_sma_for_stock_no_signals():
    # Flat price → never above SMA
    price_series = pd.Series([100.0] * 300)
    sma_periods = [20, 30, 40]
    result = best_sma_for_stock(price_series, sma_periods, forward_days=50)
    assert result is None

# Test: Picks correct SMA with best forward return
def test_best_sma_selects_highest_return():
    # Generate synthetic price with increasing trend
    base = np.linspace(100, 300, 300)
    noise = np.random.normal(0, 1, 300)
    price_series = pd.Series(base + noise)

    result = best_sma_for_stock(price_series, [10, 20, 50, 100], forward_days=50)
    assert result is not None
    assert result["Best_SMA"] in [10, 20, 50, 100]

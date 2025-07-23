"""
Equity portfolio optimizer based on hackathon_2.py.
This module provides optimized equity recommendations based on risk profile.
"""
import os
import pandas as pd
import numpy as np
import datetime

# Try to import pypfopt, but provide a fallback if it's not available
try:
    from pypfopt import EfficientFrontier, expected_returns, risk_models
    PYPFOPT_AVAILABLE = True
except ImportError:
    PYPFOPT_AVAILABLE = False
except Exception:
    PYPFOPT_AVAILABLE = False

# Define risk profiles and their corresponding filters
RISK_PROFILES = {
    "low": {
        "min_pe": 10, "max_pe": 30,
        "max_beta": 1.0,
        "sectors": ["Technology", "Finance", "Energy", "Banking"],
        "max_stocks": 25
    },
    "medium": {
        "min_pe": 10, "max_pe": 40,
        "max_beta": 1.3,
        "sectors": ["Technology", "Finance", "Energy", "Banking", "Auto"],
        "max_stocks": 20
    },
    "high": {
        "min_pe": 5, "max_pe": 50,
        "max_beta": 1.6,
        "sectors": ["Technology", "Finance", "Auto", "Pharma", "Energy"],
        "max_stocks": 12
    }
}

# Default tickers for testing when yfinance data is not available
DEFAULT_TICKERS = [
    "INFY.NS", "TCS.NS", "RELIANCE.NS", "WIPRO.NS", "TECHM.NS",
    "HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "HINDUNILVR.NS",
    "ITC.NS", "BHARTIARTL.NS", "SBIN.NS", "ADANIENT.NS", "DMART.NS",
    "PIDILITIND.NS", "TATAMOTORS.NS", "BAJAJFINSV.NS", "DIVISLAB.NS",
    "ZYDUSLIFE.NS", "RADICO.NS"
]

# Default stock data for when we can't fetch from yfinance
DEFAULT_STOCK_DATA = [
    {"ticker": "INFY.NS", "pe": 25.2, "beta": 0.8, "sector": "Technology", "market_cap": 600000000000},
    {"ticker": "TCS.NS", "pe": 27.5, "beta": 0.75, "sector": "Technology", "market_cap": 700000000000},
    {"ticker": "RELIANCE.NS", "pe": 22.1, "beta": 1.1, "sector": "Energy", "market_cap": 900000000000},
    {"ticker": "WIPRO.NS", "pe": 18.6, "beta": 0.85, "sector": "Technology", "market_cap": 300000000000},
    {"ticker": "TECHM.NS", "pe": 19.8, "beta": 0.9, "sector": "Technology", "market_cap": 250000000000},
    {"ticker": "HDFCBANK.NS", "pe": 21.3, "beta": 0.95, "sector": "Banking", "market_cap": 800000000000},
    {"ticker": "ICICIBANK.NS", "pe": 20.5, "beta": 1.05, "sector": "Banking", "market_cap": 650000000000},
    {"ticker": "AXISBANK.NS", "pe": 19.2, "beta": 1.15, "sector": "Banking", "market_cap": 400000000000},
    {"ticker": "HINDUNILVR.NS", "pe": 65.8, "beta": 0.6, "sector": "Consumer", "market_cap": 550000000000},
    {"ticker": "ITC.NS", "pe": 25.7, "beta": 0.7, "sector": "Consumer", "market_cap": 450000000000},
    {"ticker": "BHARTIARTL.NS", "pe": 28.9, "beta": 0.85, "sector": "Telecom", "market_cap": 480000000000},
    {"ticker": "SBIN.NS", "pe": 12.4, "beta": 1.25, "sector": "Banking", "market_cap": 520000000000},
    {"ticker": "ADANIENT.NS", "pe": 35.6, "beta": 1.4, "sector": "Energy", "market_cap": 350000000000},
    {"ticker": "DMART.NS", "pe": 95.3, "beta": 0.8, "sector": "Retail", "market_cap": 280000000000},
    {"ticker": "PIDILITIND.NS", "pe": 82.1, "beta": 0.7, "sector": "Chemicals", "market_cap": 180000000000},
    {"ticker": "TATAMOTORS.NS", "pe": 32.6, "beta": 1.3, "sector": "Auto", "market_cap": 220000000000},
    {"ticker": "BAJAJFINSV.NS", "pe": 35.8, "beta": 1.1, "sector": "Finance", "market_cap": 260000000000},
    {"ticker": "DIVISLAB.NS", "pe": 42.3, "beta": 0.75, "sector": "Pharma", "market_cap": 190000000000},
    {"ticker": "ZYDUSLIFE.NS", "pe": 28.7, "beta": 0.8, "sector": "Pharma", "market_cap": 150000000000},
    {"ticker": "RADICO.NS", "pe": 55.2, "beta": 0.95, "sector": "Consumer", "market_cap": 80000000000}
]

# Create a DataFrame from the default stock data
DEFAULT_STOCK_UNIVERSE = pd.DataFrame(DEFAULT_STOCK_DATA)

# Add market cap category
DEFAULT_STOCK_UNIVERSE["cap_category"] = DEFAULT_STOCK_UNIVERSE["market_cap"].apply(
    lambda mcap: "large" if mcap >= 500_000_000_000 else 
                 "mid" if mcap >= 100_000_000_000 else "small"
)

# Create default price data (simulated returns)
np.random.seed(42)  # For reproducibility
DEFAULT_PRICE_DATA = pd.DataFrame(
    {ticker: 100 * (1 + np.random.normal(0.0005, 0.015, 252)).cumprod() 
     for ticker in DEFAULT_STOCK_UNIVERSE["ticker"]}
)
DEFAULT_PRICE_DATA.index = pd.date_range(
    start=datetime.datetime.now() - datetime.timedelta(days=252),
    periods=252,
    freq='B'
)

def get_filtered_stocks(risk_profile):
    """
    Filter stocks based on risk profile.
    
    Args:
        risk_profile (str): 'low', 'medium', or 'high'
        
    Returns:
        list: List of filtered stock dictionaries
    """
    # Get filter parameters based on risk profile
    filters = RISK_PROFILES.get(risk_profile, RISK_PROFILES["medium"])
    
    # Use the default stock universe
    df = DEFAULT_STOCK_UNIVERSE.copy()
    
    # Apply filters
    filtered_df = df[
        (df["pe"] >= filters["min_pe"]) &
        (df["pe"] <= filters["max_pe"]) &
        (df["beta"] <= filters["max_beta"]) &
        (df["sector"].isin(filters["sectors"]))
    ]
    
    # Limit the number of stocks
    max_stocks = filters["max_stocks"]
    if len(filtered_df) > max_stocks:
        filtered_df = filtered_df.sort_values("beta").head(max_stocks)
    
    return filtered_df.to_dict(orient="records")

def optimize_portfolio(stock_data, risk_profile):
    """
    Optimize portfolio based on filtered stocks and risk profile.
    
    Args:
        stock_data (list): List of stock dictionaries
        risk_profile (str): 'low', 'medium', or 'high'
        
    Returns:
        dict: Dictionary with optimized weights
    """
    # Extract tickers from stock data
    tickers = [stock["ticker"] for stock in stock_data]
    
    # Use default price data for the selected tickers
    price_data = DEFAULT_PRICE_DATA[tickers].dropna(axis=1)
    
    # Calculate expected returns and covariance matrix
    mu = expected_returns.mean_historical_return(price_data)
    S = risk_models.sample_cov(price_data)
    
    # Set constraints based on risk profile
    if risk_profile == "low":
        max_weight = 0.15  # More diversification for low risk
        target_return = 0.10
    elif risk_profile == "high":
        max_weight = 0.25  # Allow more concentration for high risk
        target_return = 0.18
    else:  # medium
        max_weight = 0.20
        target_return = 0.14
    
    # Create efficient frontier
    ef = EfficientFrontier(mu, S)
    ef.add_constraint(lambda w: w <= max_weight)
    ef.add_constraint(lambda w: w >= 0)
    
    try:
        # Try to optimize for target return
        ef.efficient_return(target_return=target_return)
    except Exception:
        try:
            # Fallback to maximum Sharpe ratio
            ef = EfficientFrontier(mu, S)
            ef.add_constraint(lambda w: w <= max_weight)
            ef.add_constraint(lambda w: w >= 0)
            ef.max_sharpe()
        except Exception:
            # If all else fails, use equal weights
            weights = {ticker: 1.0/len(tickers) for ticker in tickers}
            return weights
    
    # Get the optimized weights
    weights = ef.clean_weights()
    
    # Filter out weights that are too small (less than 1%)
    weights = {k: v for k, v in weights.items() if v > 0.01}
    
    # Normalize weights to sum to 1
    total_weight = sum(weights.values())
    if total_weight > 0:
        weights = {k: v/total_weight for k, v in weights.items()}
    
    return weights

def get_equity_recommendations(risk_profile):
    """
    Get optimized equity recommendations based on risk profile.
    
    Args:
        risk_profile (str): 'low', 'medium', or 'high'
        
    Returns:
        list: List of recommended equities with weights
    """
    # Check if pypfopt is available
    if not PYPFOPT_AVAILABLE:
        print("Using simplified equity recommendations (pypfopt not available)")
        # Return simplified recommendations based on risk profile
        if risk_profile == "low":
            return [
                {"ticker": "HDFC Bank", "weight": 15.5, "sector": "Banking", "beta": 0.8},
                {"ticker": "TCS", "weight": 12.3, "sector": "Technology", "beta": 0.7},
                {"ticker": "Infosys", "weight": 10.8, "sector": "Technology", "beta": 0.8},
                {"ticker": "HUL", "weight": 9.7, "sector": "Consumer", "beta": 0.6},
                {"ticker": "ITC", "weight": 8.2, "sector": "Consumer", "beta": 0.7}
            ]
        elif risk_profile == "high":
            return [
                {"ticker": "Tata Motors", "weight": 20.5, "sector": "Auto", "beta": 1.3},
                {"ticker": "Reliance Industries", "weight": 17.8, "sector": "Energy", "beta": 1.1},
                {"ticker": "ICICI Bank", "weight": 15.2, "sector": "Banking", "beta": 1.2},
                {"ticker": "Adani Enterprises", "weight": 12.6, "sector": "Energy", "beta": 1.5},
                {"ticker": "SBI", "weight": 10.4, "sector": "Banking", "beta": 1.3}
            ]
        else:  # medium
            return [
                {"ticker": "Reliance Industries", "weight": 18.2, "sector": "Energy", "beta": 1.1},
                {"ticker": "HDFC Bank", "weight": 14.5, "sector": "Banking", "beta": 0.8},
                {"ticker": "Infosys", "weight": 12.1, "sector": "Technology", "beta": 0.8},
                {"ticker": "ICICI Bank", "weight": 10.8, "sector": "Banking", "beta": 1.2},
                {"ticker": "Bharti Airtel", "weight": 9.3, "sector": "Telecom", "beta": 0.9}
            ]
    
    # If pypfopt is available, use the full optimization
    try:
        print("Using full portfolio optimization")
        # Get filtered stocks based on risk profile
        filtered_stocks = get_filtered_stocks(risk_profile)
        
        if not filtered_stocks:
            print("No filtered stocks found, using simplified recommendations")
            return get_equity_recommendations(risk_profile)  # Recursive call will use the simplified version
        
        # Optimize portfolio
        weights = optimize_portfolio(filtered_stocks, risk_profile)
        
        # Create recommendations with weights
        recommendations = []
        for ticker, weight in weights.items():
            stock_info = next((s for s in filtered_stocks if s["ticker"] == ticker), None)
            if stock_info:
                recommendations.append({
                    "ticker": ticker,
                    "weight": round(weight * 100, 2),  # Convert to percentage
                    "sector": stock_info.get("sector", "Unknown"),
                    "beta": stock_info.get("beta", 0)
                })
        
        # Sort by weight (descending)
        recommendations.sort(key=lambda x: x["weight"], reverse=True)
        
        return recommendations
    except Exception as e:
        print(f"Error in portfolio optimization: {e}")
        print("Falling back to simplified recommendations")
        # Set PYPFOPT_AVAILABLE to False to use simplified recommendations
        global PYPFOPT_AVAILABLE
        PYPFOPT_AVAILABLE = False
        return get_equity_recommendations(risk_profile)  # Recursive call will use the simplified version

# Example usage
if __name__ == "__main__":
    for risk in ["low", "medium", "high"]:
        print(f"\nEquity recommendations for {risk} risk profile:")
        recommendations = get_equity_recommendations(risk)
        for rec in recommendations:
            print(f"{rec['ticker']}: {rec['weight']}% ({rec['sector']}, β={rec['beta']})")
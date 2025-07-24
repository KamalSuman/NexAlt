import pandas as pd
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoMonteCarloOptimizer:
    def __init__(self):
        self.script_dir = os.path.dirname(__file__)
        self.crypto_data = None
        logger.info("CryptoMonteCarloOptimizer initialized")
        
    def load_crypto_data(self):
        """Load crypto data from CSV"""
        logger.info("Loading crypto data from CSV")
        try:
            file_path = os.path.join(self.script_dir, "crypto_stats.csv")
            logger.info(f"Crypto data file path: {file_path}")
            self.crypto_data = pd.read_csv(file_path)
            logger.info(f"Loaded {len(self.crypto_data)} cryptos from CSV")
            return True
        except Exception as e:
            logger.error(f"Failed to load crypto data: {e}")
            return False
    
    def run_monte_carlo_simulation(self, num_simulations=5000):
        """Run Monte Carlo simulation for crypto portfolio"""
        if self.crypto_data is None or self.crypto_data.empty:
            return None
        
        np.random.seed(42)
        
        returns = self.crypto_data['Mean_Daily_Return'].values
        volatilities = self.crypto_data['Daily_Volatility'].values
        tickers = self.crypto_data['Ticker'].values
        
        num_assets = len(tickers)
        risk_free_rate = 0.0001
        
        all_weights = []
        all_returns = []
        all_vols = []
        all_sharpes = []
        
        for _ in range(num_simulations):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            
            port_return = np.dot(weights, returns)
            port_volatility = np.sqrt(np.dot(weights.T, np.dot(np.diag(volatilities ** 2), weights)))
            
            sharpe_ratio = (port_return - risk_free_rate) / port_volatility if port_volatility > 0 else 0
            
            all_weights.append(weights)
            all_returns.append(port_return)
            all_vols.append(port_volatility)
            all_sharpes.append(sharpe_ratio)
        
        results_df = pd.DataFrame({
            "Return": all_returns,
            "Volatility": all_vols,
            "Sharpe Ratio": all_sharpes
        })
        
        for i, ticker in enumerate(tickers):
            results_df[ticker] = [w[i] for w in all_weights]
        
        results_df_sorted = results_df.sort_values(by="Sharpe Ratio", ascending=False)
        return results_df_sorted, tickers
    
    def get_crypto_recommendations(self, investment_amount):
        """Get crypto recommendations based on investment amount"""
        logger.info(f"=== GET_CRYPTO_RECOMMENDATIONS CALLED ===")
        logger.info(f"Investment amount: ₹{investment_amount:,.0f}")
        
        if investment_amount < 10000:
            target_cryptos = 2
        elif investment_amount < 50000:
            target_cryptos = 3
        elif investment_amount < 100000:
            target_cryptos = 5
        else:
            target_cryptos = 8
        
        logger.info(f"Target number of cryptos: {target_cryptos}")
        
        if not self.load_crypto_data():
            return None
        
        # Filter to top cryptos by market cap (first entries are typically larger)
        top_cryptos = self.crypto_data.head(min(30, len(self.crypto_data)))
        self.crypto_data = top_cryptos
        
        results_df, tickers = self.run_monte_carlo_simulation()
        if results_df is None:
            return None
        
        best_portfolio = results_df.iloc[0]
        weights = best_portfolio[tickers].values
        
        # Get top weighted cryptos
        crypto_weights = list(zip(tickers, weights))
        crypto_weights.sort(key=lambda x: x[1], reverse=True)
        top_cryptos = crypto_weights[:target_cryptos]
        
        # Normalize weights
        total_weight = sum(weight for _, weight in top_cryptos)
        
        recommendations = []
        for ticker, weight in top_cryptos:
            normalized_weight = (weight / total_weight) * 100
            amount = investment_amount * (normalized_weight / 100)
            
            recommendations.append({
                'symbol': ticker.replace('-USD', ''),
                'weight': normalized_weight,
                'amount': amount
            })
        
        result = {
            'recommendations': recommendations,
            'portfolio_return': best_portfolio['Return'] * 365 * 100,
            'portfolio_volatility': best_portfolio['Volatility'] * np.sqrt(365) * 100,
            'sharpe_ratio': best_portfolio['Sharpe Ratio']
        }
        
        logger.info(f"Crypto recommendations completed: {len(recommendations)} cryptos")
        logger.info("=== GET_CRYPTO_RECOMMENDATIONS COMPLETED ===")
        return result
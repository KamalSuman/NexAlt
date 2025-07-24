import pandas as pd
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CurrencyMonteCarloOptimizer:
    def __init__(self):
        self.script_dir = os.path.dirname(__file__)
        self.currency_data = None
        logger.info("CurrencyMonteCarloOptimizer initialized")
        
    def load_currency_data(self):
        """Load currency data from CSV"""
        logger.info("Loading currency data from CSV")
        try:
            file_path = os.path.join(self.script_dir, "currency_stats_vs_inr.csv")
            logger.info(f"Currency data file path: {file_path}")
            self.currency_data = pd.read_csv(file_path)
            logger.info(f"Loaded {len(self.currency_data)} currencies from CSV")
            return True
        except Exception as e:
            logger.error(f"Failed to load currency data: {e}")
            return False
    
    def run_monte_carlo_simulation(self, num_simulations=3000):
        """Run Monte Carlo simulation for currency portfolio"""
        if self.currency_data is None or self.currency_data.empty:
            return None
        
        np.random.seed(42)
        
        returns = self.currency_data['Mean Daily Return'].values
        volatilities = self.currency_data['Daily Volatility'].values
        currencies = self.currency_data['Cuurency'].values
        
        num_assets = len(currencies)
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
        
        for i, currency in enumerate(currencies):
            results_df[currency] = [w[i] for w in all_weights]
        
        results_df_sorted = results_df.sort_values(by="Sharpe Ratio", ascending=False)
        return results_df_sorted, currencies
    
    def get_currency_recommendations(self, investment_amount):
        """Get currency recommendations based on investment amount"""
        logger.info(f"=== GET_CURRENCY_RECOMMENDATIONS CALLED ===")
        logger.info(f"Investment amount: ₹{investment_amount:,.0f}")
        
        if investment_amount < 25000:
            target_currencies = 2
        elif investment_amount < 100000:
            target_currencies = 3
        else:
            target_currencies = 5
        
        logger.info(f"Target number of currencies: {target_currencies}")
        
        if not self.load_currency_data():
            return None
        
        # Filter stable currencies (positive returns, lower volatility)
        stable_currencies = self.currency_data[
            (self.currency_data['Mean Daily Return'] >= 0) & 
            (self.currency_data['Daily Volatility'] < 0.01)
        ]
        
        if len(stable_currencies) < target_currencies:
            stable_currencies = self.currency_data.nlargest(target_currencies * 2, 'Mean Daily Return')
        
        self.currency_data = stable_currencies
        
        results_df, currencies = self.run_monte_carlo_simulation()
        if results_df is None:
            return None
        
        best_portfolio = results_df.iloc[0]
        weights = best_portfolio[currencies].values
        
        # Get top weighted currencies
        currency_weights = list(zip(currencies, weights))
        currency_weights.sort(key=lambda x: x[1], reverse=True)
        top_currencies = currency_weights[:target_currencies]
        
        # Normalize weights
        total_weight = sum(weight for _, weight in top_currencies)
        
        recommendations = []
        for currency, weight in top_currencies:
            normalized_weight = (weight / total_weight) * 100
            amount = investment_amount * (normalized_weight / 100)
            
            recommendations.append({
                'symbol': currency,
                'weight': normalized_weight,
                'amount': amount
            })
        
        result = {
            'recommendations': recommendations,
            'portfolio_return': best_portfolio['Return'] * 365 * 100,
            'portfolio_volatility': best_portfolio['Volatility'] * np.sqrt(365) * 100,
            'sharpe_ratio': best_portfolio['Sharpe Ratio']
        }
        
        logger.info(f"Currency recommendations completed: {len(recommendations)} currencies")
        logger.info("=== GET_CURRENCY_RECOMMENDATIONS COMPLETED ===")
        return result
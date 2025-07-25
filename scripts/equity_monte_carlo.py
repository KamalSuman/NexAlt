import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings
import logging
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class AdvancedMonteCarloOptimizer:
    def __init__(self):
        self.script_dir = os.path.dirname(__file__)
        self.stock_data = None
        
    def load_stock_data(self):
        """Load stock data with fallback mechanism"""
        try:
            # Try to fetch fresh data
            from fetch_stock_data import fetch_nifty100_data
            self.stock_data = fetch_nifty100_data()
            return True
        except Exception as e:
            # Fallback to existing simulation data or generate it
            try:
                # Look for existing simulation data files
                files = [f for f in os.listdir(self.script_dir) if f.startswith('nifty100_simulation_data_') and f.endswith('.csv')]
                if files:
                    latest_file = max(files)
                    file_path = os.path.join(self.script_dir, latest_file)
                    self.stock_data = pd.read_csv(file_path)
                    return True
                else:
                    # Generate simulation data from existing stock_data.csv
                    from generate_simulation_data import generate_simulation_data_from_existing
                    self.stock_data = generate_simulation_data_from_existing()
                    return True
            except Exception as e2:
                logger.error(f"Failed to load/generate simulation data: {e2}")
            
            return False
    
    def run_monte_carlo_simulation(self, num_simulations=10000):
        """Run Monte Carlo simulation based on notebook logic"""
        if self.stock_data is None or self.stock_data.empty:
            return None
        
        # Set random seed for reproducible results
        np.random.seed(42)
        
        # Convert to arrays for simulation
        returns = self.stock_data['Mean Daily Return'].values
        volatilities = self.stock_data['Daily Volatility'].values
        tickers = self.stock_data['Ticker'].values
        
        num_assets = len(tickers)
        risk_free_rate = 0.0001  # Daily risk-free return
        
        # Results containers
        all_weights = []
        all_returns = []
        all_vols = []
        all_sharpes = []
        all_vars = []
        
        for _ in range(num_simulations):
            # Generate random weights and normalize
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            
            # Expected portfolio return and volatility
            port_return = np.dot(weights, returns)
            port_volatility = np.sqrt(np.dot(weights.T, np.dot(np.diag(volatilities ** 2), weights)))
            
            # Sharpe Ratio
            sharpe_ratio = (port_return - risk_free_rate) / port_volatility if port_volatility > 0 else 0
            
            # Value at Risk (VaR) at 95% confidence
            z_score = 1.645
            port_var_95 = -(port_return - z_score * port_volatility)
            
            # Store results
            all_weights.append(weights)
            all_returns.append(port_return)
            all_vols.append(port_volatility)
            all_sharpes.append(sharpe_ratio)
            all_vars.append(port_var_95)
        
        # Convert to DataFrame
        results_df = pd.DataFrame({
            "Return": all_returns,
            "Volatility": all_vols,
            "Sharpe Ratio": all_sharpes,
            "VaR (95%)": all_vars
        })
        
        # Add weights as columns
        for i, ticker in enumerate(tickers):
            results_df[ticker] = [w[i] for w in all_weights]
        
        # Sort by Sharpe Ratio descending, then VaR ascending
        results_df_sorted = results_df.sort_values(by=["Sharpe Ratio", "VaR (95%)"], ascending=[False, True])
        
        return results_df_sorted, tickers
    
    def prune_stocks(self, current_data, target_count):
        """Prune stocks based on Monte Carlo results"""
        if len(current_data) <= target_count:
            return current_data
        
        # Temporarily set stock_data for simulation
        original_data = self.stock_data
        self.stock_data = current_data
        
        # Run Monte Carlo simulation
        results_df, tickers = self.run_monte_carlo_simulation(num_simulations=5000)
        
        # Restore original data
        self.stock_data = original_data
        
        if results_df is None:
            return current_data
        
        # Get best portfolio weights
        best_portfolio = results_df.iloc[0]
        weights = best_portfolio[tickers].values
        
        # Create stock-weight pairs and sort by weight
        stock_weights = list(zip(tickers, weights))
        stock_weights.sort(key=lambda x: x[1], reverse=True)
        
        # Select top stocks
        top_tickers = [ticker for ticker, _ in stock_weights[:target_count]]
        
        # Return filtered data
        filtered_data = current_data[current_data['Ticker'].isin(top_tickers)].reset_index(drop=True)
        return filtered_data
    
    def get_stock_recommendations(self, investment_amount):
        """Get stock recommendations with iterative pruning based on investment amount"""
        # Determine number of stocks based on investment amount
        if investment_amount < 50000:
            target_stocks = 3
        elif investment_amount < 100000:
            target_stocks = 5
        elif investment_amount < 300000:
            target_stocks = 8
        elif investment_amount < 500000:
            target_stocks = 10  
        elif investment_amount < 800000:
            target_stocks = 15      
        else:
            target_stocks = 18
        
        if not self.load_stock_data():
            return None
        
        current_stocks = self.stock_data.copy()
        
        # Iterative pruning process
        iteration = 1
        while len(current_stocks) > target_stocks:
            # Determine next pruning target
            if len(current_stocks) > target_stocks * 3:
                next_target = max(target_stocks * 2, len(current_stocks) // 2)
            elif len(current_stocks) > target_stocks * 2:
                next_target = target_stocks * 2
            else:
                next_target = target_stocks
            
            # Prune stocks
            current_stocks = self.prune_stocks(current_stocks, next_target)
            
            iteration += 1
            
            if iteration > 8:  # Safety break
                break
        
        # Set current stocks for final simulation
        self.stock_data = current_stocks
        results_df, tickers = self.run_monte_carlo_simulation(num_simulations=10000)
        
        if results_df is None:
            return None
        
        # Get best portfolio
        best_portfolio = results_df.iloc[0]
        weights = best_portfolio[tickers].values
        
        # Create recommendations with only generated data
        recommendations = []
        for i, ticker in enumerate(tickers):
            weight = weights[i]
            amount = investment_amount * weight
            
            recommendations.append({
                'symbol': ticker,
                'weight': weight * 100,
                'amount': amount
            })
        
        # Prune allocations less than 5% and redistribute
        filtered_recs = [r for r in recommendations if r['weight'] >= 5.0]
        pruned_weight = sum(r['weight'] for r in recommendations if r['weight'] < 5.0)
        
        if filtered_recs and pruned_weight > 0:
            # Redistribute pruned weight proportionally
            total_filtered_weight = sum(r['weight'] for r in filtered_recs)
            for rec in filtered_recs:
                rec['weight'] += (rec['weight'] / total_filtered_weight) * pruned_weight
                rec['amount'] = investment_amount * (rec['weight'] / 100)
        
        recommendations = filtered_recs if filtered_recs else recommendations
        recommendations.sort(key=lambda x: x['weight'], reverse=True)
        
        result = {
            'recommendations': recommendations,
            'portfolio_return': best_portfolio['Return'] * 252 * 100,
            'portfolio_volatility': best_portfolio['Volatility'] * np.sqrt(252) * 100,
            'sharpe_ratio': best_portfolio['Sharpe Ratio'],
            'var_95': best_portfolio['VaR (95%)'] * 252 * 100,
            'total_amount': investment_amount
        }
        
        return result

def main():
    """Test the advanced Monte Carlo optimizer"""
    optimizer = AdvancedMonteCarloOptimizer()
    
    test_amounts = [50000, 200000, 500000]
    
    for amount in test_amounts:
        print(f"\n{'='*80}")
        print(f"Testing with Rs.{amount:,}")
        print(f"{'='*80}")
        
        result = optimizer.get_stock_recommendations(amount)
        
        if result and result['recommendations']:
            print(f"Portfolio Return: {result['portfolio_return']:.2f}%")
            print(f"Portfolio Volatility: {result['portfolio_volatility']:.2f}%")
            print(f"Sharpe Ratio: {result['sharpe_ratio']:.3f}")
            print(f"VaR (95%): {result['var_95']:.2f}%")
            
            print(f"\nTop {len(result['recommendations'])} Recommendations:")
            for i, rec in enumerate(result['recommendations'], 1):
                print(f"{i}. {rec['symbol']}: {rec['weight']:.1f}% (Rs.{rec['amount']:,.0f})")
        else:
            print("Failed to generate recommendations")

if __name__ == "__main__":
    main()
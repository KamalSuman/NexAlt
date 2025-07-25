import pandas as pd
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)

class BondMonteCarloOptimizer:
    def __init__(self):
        self.script_dir = os.path.dirname(__file__)
        self.bond_data = None
        
    def load_bond_data(self):
        """Load bond data from CSV"""
        try:
            file_path = os.path.join(self.script_dir, "bond_daily_stats.csv")
            self.bond_data = pd.read_csv(file_path)
            return True
        except Exception as e:
            logger.error(f"Failed to load bond data: {e}")
            return False
    
    def run_monte_carlo_simulation(self, num_simulations=3000):
        """Run Monte Carlo simulation for bond portfolio"""
        if self.bond_data is None or self.bond_data.empty:
            return None
        
        np.random.seed(42)
        
        returns = self.bond_data['Mean Daily Return'].values
        volatilities = self.bond_data['Daily Volatility'].values
        names = self.bond_data['Name'].values
        symbols = self.bond_data['Symbol'].values
        
        num_assets = len(names)
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
        
        for i, name in enumerate(names):
            results_df[name] = [w[i] for w in all_weights]
        
        results_df_sorted = results_df.sort_values(by="Sharpe Ratio", ascending=False)
        
        return results_df_sorted, names, symbols
    
    def get_bond_recommendations(self, investment_amount):
        """Get bond recommendations based on investment amount"""
        if investment_amount < 20000:
            target_bonds = 2
        elif investment_amount < 50000:
            target_bonds = 3
        elif investment_amount < 100000:
            target_bonds = 5
        else:
            target_bonds = 8
        
        if not self.load_bond_data():
            return None
        
        # Filter stable bonds (lower volatility, positive returns)
        stable_bonds = self.bond_data[
            (self.bond_data['Mean Daily Return'] > 0) & 
            (self.bond_data['Daily Volatility'] < 0.005)
        ]
        
        if len(stable_bonds) < target_bonds:
            stable_bonds = self.bond_data.nlargest(target_bonds * 2, 'Mean Daily Return')
        
        self.bond_data = stable_bonds
        
        results_df, names, symbols = self.run_monte_carlo_simulation()
        if results_df is None:
            return None
        
        best_portfolio = results_df.iloc[0]
        weights = best_portfolio[names].values
        
        # Get top weighted bonds
        bond_weights = list(zip(names, symbols, weights))
        bond_weights.sort(key=lambda x: x[2], reverse=True)
        top_bonds = bond_weights[:target_bonds]
        
        # Normalize weights
        total_weight = sum(weight for _, _, weight in top_bonds)
        
        recommendations = []
        for name, symbol, weight in top_bonds:
            normalized_weight = (weight / total_weight) * 100
            amount = investment_amount * (normalized_weight / 100)
            
            recommendations.append({
                'name': name,
                'symbol': symbol,
                'weight': normalized_weight,
                'amount': amount
            })
        
        result = {
            'recommendations': recommendations,
            'portfolio_return': best_portfolio['Return'] * 365 * 100,
            'portfolio_volatility': best_portfolio['Volatility'] * np.sqrt(365) * 100,
            'sharpe_ratio': best_portfolio['Sharpe Ratio']
        }
        
        return result
    
def main():
    """Test the advanced Monte Carlo optimizer"""
    optimizer = BondMonteCarloOptimizer()
    
    test_amounts = [50000, 200000, 500000]
    
    for amount in test_amounts:
        print(f"\n{'='*80}")
        print(f"Testing with Rs.{amount:,}")
        print(f"{'='*80}")
        
        result = optimizer.get_bond_recommendations(amount)
        
        if result and result['recommendations']:
            print(f"Portfolio Return: {result['portfolio_return']:.2f}%")
            print(f"Portfolio Volatility: {result['portfolio_volatility']:.2f}%")
            print(f"Sharpe Ratio: {result['sharpe_ratio']:.3f}")
            
            print(f"\nTop {len(result['recommendations'])} Recommendations:")
            for i, rec in enumerate(result['recommendations'], 1):
                print(f"{i}. {rec['symbol']}: {rec['weight']:.1f}% (Rs.{rec['amount']:,.0f})")
        else:
            print("Failed to generate recommendations")

if __name__ == "__main__":
    main()    
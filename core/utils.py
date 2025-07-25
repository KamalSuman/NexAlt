import os
import sys
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def get_investment_allocation(profile_data):
    """
    Get investment allocation prediction for a given profile.
    
    Args:
        profile_data (dict): Dictionary containing user financial and risk profile data
    
    Returns:
        dict: Dictionary with allocation and recommended instruments,
              or None if prediction fails
    """
    try:
        # Add path to scripts directory to Python path
        scripts_dir = os.path.join(settings.BASE_DIR, 'scripts')
        if scripts_dir not in sys.path:
            sys.path.append(scripts_dir)
        
        # Import prediction module
        from prediction_allocation import predict_allocation
        
        # Get allocation prediction with recommended instruments
        result = predict_allocation(profile_data, include_instruments=True)
        
        # Get Monte Carlo recommendations for equity, crypto, and cash
        if result and 'allocation' in result:
            total_amount = profile_data.get('capital', 100000)
            
            # Add amount values to allocation
            for asset_class, percentage in result['allocation'].items():
                amount = total_amount * (percentage / 100)
                result['allocation'][asset_class] = {
                    'percentage': percentage,
                    'amount': amount
                }
            
            # Equity recommendations
            if 'equity' in result['allocation']:
                equity_amount = total_amount * (result['allocation']['equity']['percentage'] / 100)
                if equity_amount > 0:
                    from equity_monte_carlo import AdvancedMonteCarloOptimizer
                    optimizer = AdvancedMonteCarloOptimizer()
                    equity_recs = optimizer.get_stock_recommendations(equity_amount)
                    if equity_recs:
                        result['equity_recommendations'] = equity_recs['recommendations']
            
            # Crypto recommendations
            if 'crypto' in result['allocation']:
                crypto_amount = total_amount * (result['allocation']['crypto']['percentage'] / 100)
                if crypto_amount > 0:
                    from crypto_monte_carlo import CryptoMonteCarloOptimizer
                    crypto_optimizer = CryptoMonteCarloOptimizer()
                    crypto_recs = crypto_optimizer.get_crypto_recommendations(crypto_amount)
                    if crypto_recs:
                        result['crypto_recommendations'] = crypto_recs['recommendations']
            
            # Currency recommendations for cash allocation
            if 'cash' in result['allocation']:
                cash_amount = total_amount * (result['allocation']['cash']['percentage'] / 100)
                if cash_amount > 0:
                    from currency_monte_carlo import CurrencyMonteCarloOptimizer
                    currency_optimizer = CurrencyMonteCarloOptimizer()
                    currency_recs = currency_optimizer.get_currency_recommendations(cash_amount)
                    if currency_recs:
                        result['currency_recommendations'] = currency_recs['recommendations']
            
            # Bond recommendations for debt allocation
            if 'debt' in result['allocation']:
                debt_amount = total_amount * (result['allocation']['debt']['percentage'] / 100)
                if debt_amount > 0:
                    from bond_monte_carlo import BondMonteCarloOptimizer
                    bond_optimizer = BondMonteCarloOptimizer()
                    bond_recs = bond_optimizer.get_bond_recommendations(debt_amount)
                    if bond_recs:
                        result['bond_recommendations'] = bond_recs['recommendations']
        
        return result
        
    except Exception as e:
        logger.error(f"Error predicting allocation: {str(e)}")
        return None
    

def main():
    """Test the advanced Monte Carlo optimizer"""
    sample_data = {
        "age": 45,
        "income": 240000,
        "capital": 100000,
        "expenses": 100000,
        "emi": 80000,
        "liquidity_need": 0,
        "dependents": 4,
        "confidence": 0.1,
        "knowledge": 0.1,
        "comfort_with_negatives": 0,
        "market_awareness": 0.1,
        "experience": 0
    }
    result =get_investment_allocation(sample_data)
    print(f"Result: {result}")
    

if __name__ == "__main__":
    main()      
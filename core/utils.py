import os
import sys
import logging
from django.conf import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
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
    print("\n" + "="*80)
    print("🚀 GET_INVESTMENT_ALLOCATION FUNCTION CALLED")
    print("="*80)
    print(f"📊 Input profile_data: {profile_data}")
    logger.info("=== GET_INVESTMENT_ALLOCATION FUNCTION CALLED ===")
    logger.info(f"Input profile_data: {profile_data}")
    
    try:
        # Add path to scripts directory to Python path
        scripts_dir = os.path.join(settings.BASE_DIR, 'scripts')
        logger.info(f"Scripts directory: {scripts_dir}")
        if scripts_dir not in sys.path:
            sys.path.append(scripts_dir)
            logger.info("Added scripts directory to Python path")
        
        # Import prediction module
        logger.info("Importing prediction_allocation module")
        from prediction_allocation import predict_allocation
        logger.info("Successfully imported predict_allocation function")
        
        # Get allocation prediction with recommended instruments
        logger.info("Calling predict_allocation with include_instruments=True")
        result = predict_allocation(profile_data, include_instruments=True)
        logger.info(f"predict_allocation returned: {result is not None}")
        if result:
            logger.info(f"Prediction result keys: {list(result.keys())}")
        
        # Get Monte Carlo recommendations for equity, crypto, and cash
        if result and 'allocation' in result:
            total_amount = profile_data.get('capital', 100000)
            print(f"💰 Total investment amount: ₹{total_amount:,}")
            print(f"📈 Original allocation: {result['allocation']}")
            logger.info(f"Total investment amount: {total_amount}")
            logger.info(f"Original allocation: {result['allocation']}")
            
            # Add amount values to allocation
            logger.info("Converting allocation percentages to amounts")
            for asset_class, percentage in result['allocation'].items():
                amount = total_amount * (percentage / 100)
                result['allocation'][asset_class] = {
                    'percentage': percentage,
                    'amount': amount
                }
                logger.info(f"{asset_class}: {percentage}% = ₹{amount:,.0f}")
            
            # Equity recommendations
            if 'equity' in result['allocation']:
                equity_amount = total_amount * (result['allocation']['equity']['percentage'] / 100)
                logger.info(f"Equity allocation amount: ₹{equity_amount:,.0f}")
                if equity_amount > 0:
                    logger.info("Getting equity recommendations using Monte Carlo")
                    from equity_monte_carlo import AdvancedMonteCarloOptimizer
                    optimizer = AdvancedMonteCarloOptimizer()
                    equity_recs = optimizer.get_stock_recommendations(equity_amount)
                    if equity_recs:
                        result['equity_recommendations'] = equity_recs['recommendations']
                        logger.info(f"Added {len(equity_recs['recommendations'])} equity recommendations")
                    else:
                        logger.warning("No equity recommendations generated")
                else:
                    logger.info("Equity amount is 0, skipping equity recommendations")
            
            # Crypto recommendations
            if 'crypto' in result['allocation']:
                crypto_amount = total_amount * (result['allocation']['crypto']['percentage'] / 100)
                logger.info(f"Crypto allocation amount: ₹{crypto_amount:,.0f}")
                if crypto_amount > 0:
                    logger.info("Getting crypto recommendations using Monte Carlo")
                    from crypto_monte_carlo import CryptoMonteCarloOptimizer
                    crypto_optimizer = CryptoMonteCarloOptimizer()
                    crypto_recs = crypto_optimizer.get_crypto_recommendations(crypto_amount)
                    if crypto_recs:
                        result['crypto_recommendations'] = crypto_recs['recommendations']
                        logger.info(f"Added {len(crypto_recs['recommendations'])} crypto recommendations")
                    else:
                        logger.warning("No crypto recommendations generated")
                else:
                    logger.info("Crypto amount is 0, skipping crypto recommendations")
            
            # Currency recommendations for cash allocation
            if 'cash' in result['allocation']:
                cash_amount = total_amount * (result['allocation']['cash']['percentage'] / 100)
                logger.info(f"Cash allocation amount: ₹{cash_amount:,.0f}")
                if cash_amount > 0:
                    logger.info("Getting currency recommendations using Monte Carlo")
                    from currency_monte_carlo import CurrencyMonteCarloOptimizer
                    currency_optimizer = CurrencyMonteCarloOptimizer()
                    currency_recs = currency_optimizer.get_currency_recommendations(cash_amount)
                    if currency_recs:
                        result['currency_recommendations'] = currency_recs['recommendations']
                        logger.info(f"Added {len(currency_recs['recommendations'])} currency recommendations")
                    else:
                        logger.warning("No currency recommendations generated")
                else:
                    logger.info("Cash amount is 0, skipping currency recommendations")
            
            # Bond recommendations for debt allocation
            if 'debt' in result['allocation']:
                debt_amount = total_amount * (result['allocation']['debt']['percentage'] / 100)
                logger.info(f"Debt allocation amount: ₹{debt_amount:,.0f}")
                if debt_amount > 0:
                    print(f"🏦 Getting bond recommendations for ₹{debt_amount:,}")
                    logger.info("Getting bond recommendations using Monte Carlo")
                    logger.info("Attempting to import BondMonteCarloOptimizer")
                    from bond_monte_carlo import BondMonteCarloOptimizer
                    logger.info("BondMonteCarloOptimizer imported successfully")
                    
                    bond_optimizer = BondMonteCarloOptimizer()
                    logger.info("BondMonteCarloOptimizer initialized")
                    bond_recs = bond_optimizer.get_bond_recommendations(debt_amount)
                    print(f"✅ Bond recommendations completed: {bond_recs is not None}")
                    logger.info(f"Bond recommendations call completed: {bond_recs is not None}")
                    
                    if bond_recs:
                        result['bond_recommendations'] = bond_recs['recommendations']
                        print(f"🎯 Added {len(bond_recs['recommendations'])} bond recommendations")
                        logger.info(f"SUCCESS: Added {len(bond_recs['recommendations'])} bond recommendations")
                    else:
                        print("⚠️ No bond recommendations generated")
                        logger.warning("No bond recommendations generated or invalid format")


                else:
                    logger.info("Debt amount is 0, skipping bond recommendations")
        
        if result:
            logger.info(f"Final result keys: {list(result.keys())}")
            # Explicitly check for bond recommendations
            if 'bond_recommendations' in result:
                logger.info(f"CONFIRMED: Bond recommendations present with {len(result['bond_recommendations'])} items")
                if result['bond_recommendations']:
                    logger.info(f"First bond in final result: {result['bond_recommendations'][0]}")
            else:
                logger.warning("CRITICAL ISSUE: Bond recommendations missing from final result")
                logger.warning("This should not happen if debt allocation > 0")
        print(f"\n🏁 FINAL RESULT KEYS: {list(result.keys()) if result else 'None'}")
        print("="*80 + "\n")
        logger.info("=== GET_INVESTMENT_ALLOCATION COMPLETED SUCCESSFULLY ===")
        logger.info(f"Returning result with keys: {list(result.keys()) if result else 'None'}")
        return result
        
    except Exception as e:
        logger.error(f"Error predicting allocation: {str(e)}")
        logger.error(f"Exception type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None
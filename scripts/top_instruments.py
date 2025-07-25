import os
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the equity optimizer module
try:
    # First try direct import
    import sys
    import os
    
    # Add the current directory to the path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.append(script_dir)
    
    # Now try to import
    import equity_optimizer
    EQUITY_OPTIMIZER_AVAILABLE = True
except Exception:
    EQUITY_OPTIMIZER_AVAILABLE = False

# Fallback equity recommendations by risk profile
FALLBACK_EQUITY_RECOMMENDATIONS = {
    "low": [
        "HDFC Bank (15.5%)",
        "TCS (12.3%)",
        "Infosys (10.8%)",
        "HUL (9.7%)",
        "ITC (8.2%)"
    ],
    "medium": [
        "Reliance Industries (18.2%)",
        "HDFC Bank (14.5%)",
        "Infosys (12.1%)",
        "ICICI Bank (10.8%)",
        "Bharti Airtel (9.3%)"
    ],
    "high": [
        "Tata Motors (20.5%)",
        "Reliance Industries (17.8%)",
        "ICICI Bank (15.2%)",
        "Adani Enterprises (12.6%)",
        "SBI (10.4%)"
    ]
}

def get_top_instruments():
    """
    Read the top instruments Excel file and return a dictionary of top instruments by asset class.
    
    Returns:
        dict: Dictionary with asset classes as keys and lists of top instruments as values
    """
    try:
        # Get the absolute path to the Excel file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(script_dir, "top20_indian_instruments.xlsx")
        
        # Check if file exists
        if not os.path.exists(excel_path):
            return {}
        
        # Read the Excel file
        instruments_df = pd.read_excel(excel_path, sheet_name=None)
        
        # Create a dictionary to store top instruments by asset class
        top_instruments = {}
        
        # Process each sheet (assuming each sheet represents an asset class)
        for asset_class, df in instruments_df.items():
            # Clean up the asset class name (lowercase, replace spaces with underscores)
            asset_key = asset_class.lower().replace(' ', '_')
            
            # Extract the top instruments (assuming first column contains instrument names)
            if not df.empty:
                instruments = df.iloc[:, 0].tolist()
                
                # Store in dictionary
                top_instruments[asset_key] = instruments
        
        return top_instruments
    
    except Exception:
        # Return empty dictionary if there's an error
        return {}

def get_recommended_instruments(allocation, risk_profile="medium"):
    """
    Get recommended instruments based on allocation percentages.
    
    Args:
        allocation (dict): Dictionary with asset classes as keys and allocation percentages as values
        risk_profile (str): Risk profile for equity optimization ('low', 'medium', or 'high')
        
    Returns:
        dict: Dictionary with asset classes as keys and lists of recommended instruments as values
    """
    logger.info(f"=== GET_RECOMMENDED_INSTRUMENTS CALLED ===")
    logger.info(f"Allocation: {allocation}")
    logger.info(f"Risk profile: {risk_profile}")
    
    # Get all top instruments from Excel file
    logger.info("Loading top instruments from Excel file")
    all_instruments = get_top_instruments()
    logger.info(f"Loaded instruments for {len(all_instruments)} asset classes")
    
    # Create a dictionary to store recommended instruments
    recommended = {}
    logger.info("Processing each asset class for recommendations...")
    
    # For each asset class in the allocation
    for asset_class, percentage in allocation.items():
        # Skip if percentage is 0 or negative
        if percentage <= 0:
            continue
        
        # Special handling for equity asset class
        if asset_class == 'equity' and percentage > 0:
            # First try using the optimizer if available
            if EQUITY_OPTIMIZER_AVAILABLE:
                try:
                    # Get optimized equity recommendations
                    equity_recs = equity_optimizer.get_equity_recommendations(risk_profile)
                    
                    if equity_recs:
                        # Convert to the expected format
                        recommended[asset_class] = [
                            f"{rec['ticker']} ({rec['weight']}%)" for rec in equity_recs
                        ]
                        continue  # Skip the standard processing below
                except Exception:
                    pass  # Fall through to fallback
            
            # Use fallback equity recommendations if optimizer failed or not available
            recommended[asset_class] = FALLBACK_EQUITY_RECOMMENDATIONS.get(risk_profile, FALLBACK_EQUITY_RECOMMENDATIONS["medium"])
            continue  # Skip the standard processing below
        
        # Standard processing for other asset classes or if equity optimization failed
        if asset_class not in all_instruments:
            continue
        
        # Get the instruments for this asset class
        instruments = all_instruments.get(asset_class, [])
        
        # Determine how many instruments to recommend based on allocation percentage
        if percentage >= 20:
            num_instruments = min(5, len(instruments))
        elif percentage >= 10:
            num_instruments = min(3, len(instruments))
        else:
            num_instruments = min(2, len(instruments))
        
        # Get the top N instruments
        recommended[asset_class] = instruments[:num_instruments]
    
    logger.info(f"Final recommendations for {len(recommended)} asset classes")
    logger.info("=== GET_RECOMMENDED_INSTRUMENTS COMPLETED ===")
    return recommended

# Example usage
if __name__ == "__main__":
    # Example allocation
    allocation = {
        'equity': 40,
        'debt': 30,
        'gold': 10,
        'real_estate': 10,
        'crypto': 5,
        'cash': 5
    }
    
    # Get recommended instruments
    recommended = get_recommended_instruments(allocation)
    
    # Print recommendations
    print("Recommended Instruments:")
    for asset_class, instruments in recommended.items():
        print(f"{asset_class.capitalize()} ({allocation[asset_class]}%):")
        for instrument in instruments:
            print(f"  - {instrument}")
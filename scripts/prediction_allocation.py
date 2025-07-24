import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from joblib import load
from scipy.special import softmax
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path to the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
logger.info(f"Script directory: {SCRIPT_DIR}")

# Load model and scaler with absolute paths
model_path = os.path.join(SCRIPT_DIR, "trained_allocation_model.joblib")
scaler_path = os.path.join(SCRIPT_DIR, "scaler.joblib")
logger.info(f"Loading model from: {model_path}")
logger.info(f"Loading scaler from: {scaler_path}")

model = load(model_path)
scaler = load(scaler_path)
logger.info("Model and scaler loaded successfully")

# Asset classes
asset_classes = ['equity', 'debt', 'gold', 'real_estate', 'crypto', 'cash']

# Import top instruments module (will be imported when needed)
top_instruments_module = None

def predict_allocation(input_data, include_instruments=True):
    """
    Predict asset allocation based on input data.
    
    Args:
        input_data (dict): Dictionary containing user financial and risk profile data
            with keys: age, income, capital, expenses, emi, liquidity_need, dependents,
            confidence, knowledge, comfort_with_negatives, market_awareness, experience
        include_instruments (bool): Whether to include recommended instruments in the response
    
    Returns:
        dict: Dictionary with allocation percentages and recommended instruments
    """
    logger.info("=== PREDICT_ALLOCATION FUNCTION CALLED ===")
    logger.info(f"Input data: {input_data}")
    logger.info(f"Include instruments: {include_instruments}")
    
    # Convert to DataFrame and scale
    logger.info("Converting input data to DataFrame")
    X_input = pd.DataFrame([input_data])
    logger.info(f"DataFrame shape: {X_input.shape}")
    logger.info(f"DataFrame columns: {list(X_input.columns)}")
    
    logger.info("Scaling input data")
    X_scaled = scaler.transform(X_input)
    logger.info(f"Scaled data shape: {X_scaled.shape}")
    
    # Predict
    logger.info("Making prediction with ML model")
    preds = model.predict(X_scaled)
    logger.info(f"Raw predictions: {preds}")
    logger.info(f"Predictions shape: {preds.shape}")
    
    # Clip to ensure no negatives and re-normalize
    logger.info("Clipping negative values and normalizing")
    predicted_weights = np.clip(preds, 0, None)
    logger.info(f"Clipped weights: {predicted_weights}")
    normalized_weights = predicted_weights / predicted_weights.sum()
    normalized_weights = normalized_weights[0]  # Get first row
    logger.info(f"Normalized weights: {normalized_weights}")
    
    # Create result dictionary for allocation percentages
    logger.info("Creating allocation dictionary")
    allocation = {}
    for asset, weight in zip(asset_classes, normalized_weights):
        percentage = round(float(weight) * 100, 2)
        allocation[asset] = percentage
        logger.info(f"{asset}: {percentage}%")
    
    # Create the response dictionary
    logger.info("Creating response dictionary")
    response = {
        "allocation": allocation
    }
    logger.info(f"Base response created with allocation: {allocation}")
    
    # Add recommended instruments if requested
    if include_instruments:
        logger.info("Including recommended instruments")
        try:
            # Import the top_instruments module dynamically to avoid circular imports
            global top_instruments_module
            if top_instruments_module is None:
                logger.info("Importing top_instruments module")
                import top_instruments
                top_instruments_module = top_instruments
                logger.info("top_instruments module imported successfully")
            
            # Determine risk profile based on user's risk tolerance parameters
            risk_profile = "medium"  # Default
            
            # Use comfort_with_negatives, confidence, and experience to determine risk profile
            comfort = input_data.get("comfort_with_negatives", 0)
            confidence = input_data.get("confidence", 0)
            experience = input_data.get("experience", 0)
            
            risk_score = (comfort * 0.4 + confidence * 0.3 + experience * 0.3)
            logger.info(f"Risk calculation: comfort={comfort}, confidence={confidence}, experience={experience}")
            logger.info(f"Risk score: {risk_score}")
            
            if risk_score < 0.3:
                risk_profile = "low"
            elif risk_score > 0.6:
                risk_profile = "high"
            
            logger.info(f"Determined risk profile: {risk_profile}")
            
            # Get recommended instruments based on allocation and risk profile
            logger.info(f"Getting recommended instruments for risk profile: {risk_profile}")
            instruments = top_instruments_module.get_recommended_instruments(allocation, risk_profile)
            response["recommended_instruments"] = instruments
            response["risk_profile"] = risk_profile
            logger.info(f"Added recommended instruments: {list(instruments.keys()) if instruments else 'None'}")
        except Exception as e:
            # If there's an error getting instruments, just continue without them
            logger.error(f"Error getting recommended instruments: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
    
    logger.info(f"Final response keys: {list(response.keys())}")
    logger.info("=== PREDICT_ALLOCATION COMPLETED ===")
    return response

# Example usage (only runs when script is executed directly)
if __name__ == "__main__":
    # Sample input for testing
    sample_input = {
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
    
    # Get prediction
    result = predict_allocation(sample_input)
    
    # Display allocation
    print("Predicted Asset Allocation:")
    for asset, percentage in result["allocation"].items():
        print(f"{asset}: {percentage:.2f}%")
    
    # Display recommended instruments
    if "recommended_instruments" in result:
        print("\nRecommended Instruments:")
        for asset_class, instruments in result["recommended_instruments"].items():
            print(f"\n{asset_class.capitalize()} ({result['allocation'][asset_class]}%):")
            for instrument in instruments:
                print(f"  - {instrument}")

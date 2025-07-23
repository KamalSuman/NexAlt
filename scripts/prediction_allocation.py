import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from joblib import load
from scipy.special import softmax
import os

# Get the absolute path to the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model and scaler with absolute paths
model = load(os.path.join(SCRIPT_DIR, "trained_allocation_model.joblib"))
scaler = load(os.path.join(SCRIPT_DIR, "scaler.joblib"))

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
    # Convert to DataFrame and scale
    X_input = pd.DataFrame([input_data])
    X_scaled = scaler.transform(X_input)
    
    # Predict
    predicted_raw = model.predict(X_scaled)[0]
    normalized_weights = softmax(predicted_raw)
    
    # Create result dictionary for allocation percentages
    allocation = {}
    for asset, weight in zip(asset_classes, normalized_weights):
        allocation[asset] = round(float(weight) * 100, 2)  # Convert to percentage with 2 decimal places
    
    # Create the response dictionary
    response = {
        "allocation": allocation
    }
    
    # Add recommended instruments if requested
    if include_instruments:
        try:
            # Import the top_instruments module dynamically to avoid circular imports
            global top_instruments_module
            if top_instruments_module is None:
                import top_instruments
                top_instruments_module = top_instruments
            
            # Determine risk profile based on user's risk tolerance parameters
            risk_profile = "medium"  # Default
            
            # Use comfort_with_negatives, confidence, and experience to determine risk profile
            risk_score = (input_data.get("comfort_with_negatives", 0) * 0.4 + 
                         input_data.get("confidence", 0) * 0.3 + 
                         input_data.get("experience", 0) * 0.3)
            
            if risk_score < 0.3:
                risk_profile = "low"
            elif risk_score > 0.6:
                risk_profile = "high"
            
            # Get recommended instruments based on allocation and risk profile
            instruments = top_instruments_module.get_recommended_instruments(allocation, risk_profile)
            response["recommended_instruments"] = instruments
            response["risk_profile"] = risk_profile
        except Exception:
            # If there's an error getting instruments, just continue without them
            pass
    
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

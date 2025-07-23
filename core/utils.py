import os
import sys
from django.conf import settings

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
        return result
        
    except Exception as e:
        # Log the error (in a real app, use proper logging)
        print(f"Error predicting allocation: {str(e)}")
        return None
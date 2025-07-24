from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import logging

from .models import InvestmentProfile
from .serializers import InvestmentProfileSerializer
from .utils import get_investment_allocation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def home(request):
    logger.info("=== HOME VIEW CALLED ===")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request path: {request.path}")
    return render(request, 'core/home.html')

def investment_form(request):
    """
    Display the investment profile form.
    """
    logger.info("=== INVESTMENT FORM VIEW CALLED ===")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request path: {request.path}")
    return render(request, 'core/investment_form.html')

def allocation_result(request, profile_id):
    """
    Display the allocation results for a specific profile.
    """
    logger.info("=== ALLOCATION RESULT VIEW CALLED ===")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request path: {request.path}")
    logger.info(f"Profile ID: {profile_id}")
    
    try:
        logger.info(f"Fetching profile with ID: {profile_id}")
        profile = InvestmentProfile.objects.get(pk=profile_id)
        logger.info(f"Profile found: Age={profile.age}, Income={profile.income}, Capital={profile.capital}")
        
        # Convert model instance to dictionary for prediction
        profile_data = {
            'age': profile.age,
            'income': profile.income,
            'capital': profile.capital,
            'expenses': profile.expenses,
            'emi': profile.emi,
            'liquidity_need': profile.liquidity_need,
            'dependents': profile.dependents,
            'confidence': profile.confidence,
            'knowledge': profile.knowledge,
            'comfort_with_negatives': profile.comfort_with_negatives,
            'market_awareness': profile.market_awareness,
            'experience': profile.experience,
        }
        logger.info(f"Profile data prepared: {profile_data}")
        
        # Get allocation prediction
        logger.info("Calling get_investment_allocation function...")
        result = get_investment_allocation(profile_data)
        logger.info(f"Allocation result received: {result is not None}")
        if result:
            logger.info(f"Result keys: {list(result.keys())}")
            if 'allocation' in result:
                logger.info(f"Allocation: {result['allocation']}")
        
        if not result:
            # If prediction fails, create a default allocation
            logger.warning("Prediction failed, using default allocation")
            result = {
                'allocation': {
                    'equity': 20,
                    'debt': 30,
                    'gold': 15,
                    'real_estate': 15,
                    'crypto': 5,
                    'cash': 15
                }
            }
            logger.info(f"Default allocation set: {result['allocation']}")
        
        # Prepare context for template
        context = {
            'profile': profile,
            'allocation': result['allocation']
        }
        
        # Add recommended instruments if available
        if 'recommended_instruments' in result:
            context['recommended_instruments'] = result['recommended_instruments']
        
        # Add equity recommendations if available
        if 'equity_recommendations' in result:
            context['equity_recommendations'] = result['equity_recommendations']
        
        # Add crypto recommendations if available
        if 'crypto_recommendations' in result:
            context['crypto_recommendations'] = result['crypto_recommendations']
            logger.info(f"Added {len(result['crypto_recommendations'])} crypto recommendations")
        else:
            logger.info("No crypto recommendations available")
        
        # Add currency recommendations if available
        if 'currency_recommendations' in result:
            context['currency_recommendations'] = result['currency_recommendations']
            logger.info(f"Added {len(result['currency_recommendations'])} currency recommendations")
        else:
            logger.info("No currency recommendations available")
        
        # Add bond recommendations if available
        if 'bond_recommendations' in result:
            context['bond_recommendations'] = result['bond_recommendations']
            logger.info(f"Added {len(result['bond_recommendations'])} bond recommendations")
        else:
            logger.info("No bond recommendations available")
        
        # Add risk profile if available
        if 'risk_profile' in result:
            context['risk_profile'] = result['risk_profile']
            logger.info(f"Risk profile: {result['risk_profile']}")
        
        logger.info(f"Final context keys: {list(context.keys())}")
        logger.info("Rendering allocation_result.html template")
        return render(request, 'core/allocation_result.html', context)
        
    except InvestmentProfile.DoesNotExist:
        # Redirect to form if profile doesn't exist
        logger.error(f"Profile with ID {profile_id} not found")
        return redirect('investment_form')
    except Exception as e:
        logger.error(f"Error in allocation_result view: {str(e)}")
        return redirect('investment_form')

@api_view(['POST'])
def create_investment_profile(request):
    """
    Create a new investment profile from the provided data.
    
    Expected JSON format:
    {
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
    """
    print("\n" + "="*80)
    print("📡 CREATE INVESTMENT PROFILE API CALLED")
    print("="*80)
    print(f"📝 Request data: {request.data}")
    logger.info("=== CREATE INVESTMENT PROFILE API CALLED ===")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request data: {request.data}")
    
    if request.method == 'POST':
        logger.info("Creating serializer with request data")
        serializer = InvestmentProfileSerializer(data=request.data)
        logger.info(f"Serializer validation: {serializer.is_valid()}")
        
        if serializer.is_valid():
            # Save the investment profile
            logger.info("Saving investment profile to database")
            profile = serializer.save()
            logger.info(f"Profile saved with ID: {profile.id}")
            
            # Get the profile data for prediction
            profile_data = serializer.data
            profile_id = profile.id
            logger.info(f"Profile data for prediction: {profile_data}")
            
            # Get allocation prediction using utility function
            logger.info("Calling get_investment_allocation from API")
            result = get_investment_allocation(profile_data)
            logger.info(f"API allocation result: {result is not None}")
            
            if result:
                # Return the allocation with the profile data
                response_data = {
                    'profile': serializer.data,
                    'result_url': request.build_absolute_uri(f'/allocation-result/{profile_id}/')
                }
                # Add allocation and recommended instruments to the response
                response_data.update(result)
                print(f"✅ API SUCCESS: Returning response with {len(response_data)} keys")
                print(f"🔑 Response keys: {list(response_data.keys())}")
                print("="*80 + "\n")
                logger.info(f"API returning successful response with {len(response_data)} keys")
                logger.info(f"Final response keys: {list(response_data.keys())}")
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                # If prediction fails, just return the profile
                logger.warning("API prediction failed, returning profile only")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            # For form submissions, redirect to the allocation result page
            return redirect('allocation_result', profile_id=profile_id)
        
        logger.error(f"Serializer validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    logger.error("Invalid request method for create_investment_profile")
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

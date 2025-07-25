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

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'core/home.html')

def investment_form(request):
    """
    Display the investment profile form.
    """
    return render(request, 'core/investment_form.html')

def allocation_result(request, profile_id):
    """
    Display the allocation results for a specific profile.
    """
    try:
        profile = InvestmentProfile.objects.get(pk=profile_id)
        
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
        
        # Get allocation prediction
        result = get_investment_allocation(profile_data)
        
        if not result:
            # If prediction fails, create a default allocation
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
        
        # Prepare context for template
        context = {
            'profile': profile,
            'allocation': result['allocation']
        }
        
        # Add recommended instruments if available
        if 'recommended_instruments' in result:
            context['recommended_instruments'] = result['recommended_instruments']
        if 'equity_recommendations' in result:
            context['equity_recommendations'] = result['equity_recommendations']
        if 'crypto_recommendations' in result:
            context['crypto_recommendations'] = result['crypto_recommendations']
        if 'currency_recommendations' in result:
            context['currency_recommendations'] = result['currency_recommendations']
        if 'bond_recommendations' in result:
            context['bond_recommendations'] = result['bond_recommendations']
        if 'risk_profile' in result:
            context['risk_profile'] = result['risk_profile']
        
        return render(request, 'core/allocation_result.html', context)
        
    except InvestmentProfile.DoesNotExist:
        logger.error(f"Profile with ID {profile_id} not found")
        return redirect('investment_form')
    except Exception as e:
        logger.error(f"Error in allocation_result view: {str(e)}")
        return redirect('investment_form')

@api_view(['POST'])
def create_investment_profile(request):
    """
    Create a new investment profile from the provided data.
    """
    if request.method == 'POST':
        serializer = InvestmentProfileSerializer(data=request.data)
        
        if serializer.is_valid():
            profile = serializer.save()
            profile_data = serializer.data
            profile_id = profile.id
            
            # Get allocation prediction using utility function
            result = get_investment_allocation(profile_data)
            
            if result:
                response_data = {
                    'profile': serializer.data,
                    'result_url': request.build_absolute_uri(f'/allocation-result/{profile_id}/')
                }
                response_data.update(result)
                logger.info(f"API SUCCESS: Profile {profile_id} created with allocation")
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return redirect('allocation_result', profile_id=profile_id)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

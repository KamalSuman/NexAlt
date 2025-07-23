from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from .models import Project, InvestmentProfile
from .serializers import InvestmentProfileSerializer
from .utils import get_investment_allocation

def home(request):
    projects = Project.objects.all()
    return render(request, 'core/home.html', {'projects': projects})

class ProjectListView(ListView):
    model = Project
    template_name = 'core/project_list.html'
    context_object_name = 'projects'

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'core/project_detail.html'

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
            'experience': profile.experience
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
        
        # Add risk profile if available
        if 'risk_profile' in result:
            context['risk_profile'] = result['risk_profile']
        
        return render(request, 'core/allocation_result.html', context)
        
    except InvestmentProfile.DoesNotExist:
        # Redirect to form if profile doesn't exist
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
    if request.method == 'POST':
        serializer = InvestmentProfileSerializer(data=request.data)
        if serializer.is_valid():
            # Save the investment profile
            profile = serializer.save()
            
            # Get the profile data for prediction
            profile_data = serializer.data
            profile_id = profile.id
            
            # For API requests, return JSON response
            if request.accepted_renderer.format == 'json':
                # Get allocation prediction using utility function
                result = get_investment_allocation(profile_data)
                
                if result:
                    # Return the allocation with the profile data
                    response_data = {
                        'profile': serializer.data,
                        'result_url': request.build_absolute_uri(f'/allocation-result/{profile_id}/')
                    }
                    # Add allocation and recommended instruments to the response
                    response_data.update(result)
                    return Response(response_data, status=status.HTTP_201_CREATED)
                else:
                    # If prediction fails, just return the profile
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            # For form submissions, redirect to the allocation result page
            return redirect('allocation_result', profile_id=profile_id)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

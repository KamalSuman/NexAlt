from rest_framework import serializers
from .models import InvestmentProfile

class InvestmentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentProfile
        fields = [
            'age', 'income', 'capital', 'expenses', 'emi', 
            'liquidity_need', 'dependents', 'confidence', 
            'knowledge', 'comfort_with_negatives', 
            'market_awareness', 'experience'
        ]
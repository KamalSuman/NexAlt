from django.contrib import admin
from .models import InvestmentProfile

@admin.register(InvestmentProfile)
class InvestmentProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'age', 'income', 'capital', 'dependents', 'created_at')
    list_filter = ('created_at', 'age', 'dependents')
    fieldsets = (
        ('Personal Information', {
            'fields': ('age', 'dependents')
        }),
        ('Financial Information', {
            'fields': ('income', 'capital', 'expenses', 'emi', 'liquidity_need')
        }),
        ('Risk Profile', {
            'fields': ('confidence', 'knowledge', 'comfort_with_negatives', 'market_awareness', 'experience')
        }),
    )

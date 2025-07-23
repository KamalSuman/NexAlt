from django.contrib import admin
from .models import Project, InvestmentProfile

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')

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

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('investment/', views.investment_form, name='investment_form'),
    path('allocation-result/<int:profile_id>/', views.allocation_result, name='allocation_result'),
    path('api/investment-profile/', views.create_investment_profile, name='create_investment_profile'),
]
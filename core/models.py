from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class InvestmentProfile(models.Model):
    age = models.IntegerField()
    income = models.FloatField()
    capital = models.FloatField()
    expenses = models.FloatField()
    emi = models.FloatField()
    liquidity_need = models.FloatField()
    dependents = models.IntegerField()
    confidence = models.FloatField()
    knowledge = models.FloatField()
    comfort_with_negatives = models.FloatField()
    market_awareness = models.FloatField()
    experience = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Investment Profile {self.id}"

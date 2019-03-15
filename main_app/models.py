from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Trip(models.Model):
    base_city = models.CharField(max_length=100)
    budget = models.IntegerField()
    date_from = models.DateField('From')
    date_to = models.DateField('To')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"base_city: {self.base_city}, budget: ${budget}, from: {date_from}, to: {date_to}"


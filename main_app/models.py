from django.db import models
from django.contrib.auth.models import User

import urllib3
import xml

skyscanner_api = 'prtl6749387986743898559646983194'
url = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/FR/eur/en-US/uk/us/anytime/anytime?apikey=prtl6749387986743898559646983194'

# Create your models here.
class Trip(models.Model):
    base_city = models.CharField(max_length=100)
    budget = models.IntegerField()
    date_from = models.DateField('From')
    date_to = models.DateField('To')

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"base_city: {self.base_city}, budget: ${budget}, from: {date_from}, to: {date_to}"


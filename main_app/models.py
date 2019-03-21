from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.urls import reverse
import urllib3
import xml
import datetime


# Create your models here.

class Airport(models.Model):
    name = models.CharField(max_length = 100)
    IATA_code = models.CharField(max_length = 3)

    def __str__(self):
        return f"{self.name} // {self.IATA_code}"

class Trip(models.Model):
    name = models.CharField(max_length = 250, default = 'My Trip')
    budget = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length = 3, default = 'LAX')

    def __str__(self):
        return f"budget: ${self.budget}"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'trip_id': self.id, 'airport_code': self.origin})

class Hotel(models.Model):
    name = models.CharField(max_length = 250)
    address = models.CharField(max_length = 250)
    check_in = models.CharField(max_length = 100)
    check_out = models.CharField(max_length = 100)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    price = models.FloatField()
    
    def __str__(self):
        return f"{self.name} // {self.price}"

class Flight(models.Model):
    departure_date = models.DateField()
    origin = models.CharField(max_length = 3, default = 'LAX')
    destination = models.CharField(max_length = 3, default = 'LAX')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    price = models.FloatField()
    
    def __str__(self):
        return f"Depart Date: {self.departure_date}, Price: {self.price}, Origin: {self.origin}, Destination: {self.destination}"

class Restaurant(models.Model):
    name = models.CharField(max_length =  250)
    address = models.CharField(max_length =  250)
    cuisine = models.CharField(max_length =  250)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    date_time = models.DateTimeField()
    # trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} // {self.price}"

class Event (models.Model):
    name = models.CharField(max_length =  250)
    address = models.CharField(max_length =  250)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    date_time = models.DateTimeField()
    # trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} // {self.price}"

class Attraction (models.Model):
    name = models.CharField(max_length =  250)
    address =  models.CharField(max_length =  250)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    date_time = models.DateTimeField()
    # trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} // {self.price}"

class DressCode(models.Model):
    type = models.CharField(max_length = 250)

    def __str__(self):
        return self.type

class Suitcase(models.Model):
    item_name = models.CharField(max_length = 100)
    quantity = models.IntegerField(default=1)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
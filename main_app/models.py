from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
# Create your models here.

class Airport(models.Model):
    name = models.CharField(max_length = 100)
    IATA_code = models.CharField(max_length = 3)

    def __str__(self):
        return f"{self.name} // {self.IATA_code}"

class Destination(models.Model):
    departure_date = models.DateField()
    return_date = models.DateField()
    # destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    def __str__(self):
        return f"Depart Date: {self.departure_date}, Return Date: {self.return_date}, Price: {self.price}"

class Hotel(models.Model):
    name = models.CharField(max_length = 250)
    address = models.CharField(max_length = 250)
    check_in = models.DateField ()
    check_out = models.DateField ()
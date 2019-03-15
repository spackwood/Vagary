from django.contrib import admin
from .models import Restaurant, Hotel, Event, Attraction, Airport, Trip, Destination
# Register your models here.
admin.site.register(Destination)
admin.site.register(Restaurant)
admin.site.register(Hotel)
admin.site.register(Attraction)
admin.site.register(Event)
admin.site.register(Trip)
admin.site.register(Airport)
from django.contrib import admin
from .models import Destination, Restaurant, Hotel, Event, Attraction

# Register your models here.
admin.site.register(Destination)
admin.site.register(Restaurant)
admin.site.register(Hotel)
admin.site.register(Attraction)
admin.site.register(Event)
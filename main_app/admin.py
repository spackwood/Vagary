from django.contrib import admin
from .models import Hotel, Trip, Flight
# Register your models here.
admin.site.register(Flight)
admin.site.register(Hotel)
admin.site.register(Trip)
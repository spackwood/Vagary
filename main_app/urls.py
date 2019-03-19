from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', views.signup, name='signup'),
    path('destinations/search/', views.destinations, name = "destination_search"),
    path('<airport_code>/hotels/', views.hotel_search, name = "hotel_search"), 
    path('<airport_code>/flights/', views.flight_search, name = "flight_search"),
    path('flights/add/', views.flight_add, name = "flight_add"),
    path('hotels/add/', views.hotel_add, name = "hotel_add"),
]
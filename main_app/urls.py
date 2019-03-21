from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', views.signup, name='signup'),
    path('destinations/search/', views.destinations, name = "destination_search"),
    path('<int:trip_id>/<airport_code>/hotels/', views.hotel_search, name = "hotel_search"), 
    path('<int:trip_id>/<airport_code>/flights/', views.flight_search, name = "flight_search"),
    path('<int:trip_id>/<airport_code>/flights/add/', views.flight_add, name = "flight_add"),
    path('<int:trip_id>/<airport_code>/hotels/add/', views.hotel_add, name = "hotel_add"),
    path('trips/', views.trip_list, name='view_trips'),
    path('trips/create/', views.CreateTrip.as_view(), name="create_trip"),
    path('trips/<int:trip_id>/<airport_code>/', views.trips_detail, name="detail"),
    path('trips/<int:pk>/<airport_code>/delete/', views.TripDelete.as_view(), name='delete_trip'),
    path('trips/<int:pk>/<airport_code>/edit/', views.TripEdit.as_view(), name='edit_trip'),
    path('profile/trip/', views.SaveTrip, name="save_trip"),
    path('trips/<int:trip_id>/<airport_code>/add_luggage_items/', views.add_luggage_items, name="add_luggage_items"),
    path('trips/<int:trip_id>/<airport_code>/<int:item_id>/add/', views.add, name = "add_luggage_quantity"),
    path('trips/<int:trip_id>/<airport_code>/<int:item_id>/subtract/', views.subtract, name = "subtract_luggage_quantity")
]
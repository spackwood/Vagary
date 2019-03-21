from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from amadeus import Client, ResponseError
from amadeus.client.decorator import Decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login
import os
import requests
from datetime import datetime, date
from .models import Trip, Hotel, Flight, User, Suitcase
from .forms import LuggageForm

# Create your views here.
amadeus = Client(
    client_id=os.environ.get("AMADEUS_CLIENT_ID"),
    client_secret=os.environ.get("AMADEUS_CLIENT_SECRET")
)
data = requests.get("http://iatacodes.org/api/v6/cities?api_key=c05152c1-441f-430e-9c6c-54dca70f1427")
res = data.json()['response']


def home(request):
    return render(request, 'home.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid credentials - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def destinations(request):
    origin = request.POST.get('origin')
    d_date = request.POST.get('d_date')
    budget = float(request.POST.get('budget'))

    check_date = datetime.strptime(d_date, '%Y-%m-%d').date()
    
    if request.user.is_authenticated:
        trip = Trip(budget=budget, user=request.user, origin=origin)
        trip.save()
    else:
        return redirect('login')
    
    if check_date < date.today():
       return redirect('home')

    try:
        search_list = amadeus.shopping.flight_destinations.get(
            origin=origin,
            departureDate=d_date
            ).data
        destinations = []
        for destination in search_list:
            d_price = float(destination['price']['total'])
            if d_price <= budget/2:
                destinations.append(destination)
        return render(request, 'destinations/search.html', {
        'destinations': destinations, 
        'budget': budget, 'origin': origin, 
        'departure_date':d_date, 
        "trip": trip,
        'iata': res
        })
    except: 
        return render (request, 'error.html')

def hotel_search(request, trip_id, airport_code):
    budget = float(request.POST.get('budget'))
    trip = Trip.objects.get(id=trip_id)
    hotel_search = amadeus.shopping.hotel_offers.get(cityCode=airport_code).data

    hotels = []
    for hotel in hotel_search:
        h_price = float(hotel['offers'][0]['price']['total'])
        if h_price <= budget/3:
            hotels.append(hotel) 
    return render(request, 'hotels/search.html', {'hotels' : hotels, 'trip': trip, 'airport_code': airport_code})

def flight_search(request, trip_id, airport_code):
    budget = float(request.POST.get('budget'))
    origin = request.POST.get('origin')
    departure_date = request.POST.get('departure_date') or request.POST.get('return_date')
    trip = Trip.objects.get(id=trip_id)


    flight_search = amadeus.shopping.flight_offers.get(destination=airport_code, origin=origin, departureDate=departure_date).data
    flights = []
    for flight in flight_search:
        f_price = float(flight['offerItems'][0]['price']['total'])
        f_origin = flight['offerItems'][0]['services'][0]['segments'][0]['flightSegment']['departure']['iataCode']
        f_destination = flight['offerItems'][0]['services'][0]['segments'][0]['flightSegment']['arrival']['iataCode']
        if f_price <= budget/3 and f_origin == origin and f_destination == airport_code:
            flights.append(flight)
    return render(request, 'flights/search.html', {
        'flights': flights, 
        'trip': trip, 
        'departure_date': departure_date, 
        'airport_code': airport_code,
        'iata': res
        })

def flight_add(request, trip_id, airport_code):
    price = request.POST.get('price')
    trip = Trip.objects.get(id=trip_id)
    origin = request.POST.get('origin')
    destination = request.POST.get('destination')
    departure_date = request.POST.get('departure_date')
    airport_code = airport_code
        
    current_flight = Flight.objects.create(
        departure_date = departure_date,
        destination = destination,
        price = price,
        origin = origin,
        trip = trip,
        )
    if trip.origin == airport_code:
        return redirect(f'/trips/{trip.id}/{airport_code}')
    else: 
        return redirect(f'/trips/{trip.id}/{origin}')

def hotel_add(request, trip_id, airport_code):
    price = request.POST.get('price')
    name = request.POST.get('name')
    check_out = request.POST.get('check_out')
    check_in = request.POST.get('check_in')
    street = request.POST.get('street')
    city = request.POST.get('city')
    trip = Trip.objects.get(id=trip_id)
    origin = airport_code

    current_hotel = Hotel.objects.create(
        name = name,
        check_out = check_out,
        check_in = check_in, 
        address = street + city,
        price = price,
        trip = trip
        )

    print(current_hotel.trip)
    
    return redirect(f'/trips/{trip.id}/{origin}')

class CreateTrip(LoginRequiredMixin, CreateView):
    model = Trip
    fields = ['name', 'budget', 'origin']
    def form_valid(self, form):
        form.instance.user = self.request.user   # Let the CreateView do its job as usual
        return super().form_valid(form)

def trips_detail(request, trip_id, airport_code):
    trip = Trip.objects.get(id=trip_id)

    if airport_code == trip.origin: 
        origin = airport_code
    else: 
        origin = trip.origin
    
    try:
        depart_flight = Flight.objects.get(trip=trip, origin=origin)
    except:
        depart_flight = None

    try: 
        return_flight = Flight.objects.get(trip=trip, destination=origin)
    except:
        return_flight = None

    try:
        hotel = Hotel.objects.get(trip=trip)
    except:
        hotel = None
    
    try: 
        trip_days = (return_flight.departure_date - depart_flight.departure_date).days
        trip_nights = trip_days - 1
        total_tops = trip_days + 2
        total_bottoms = trip_days - 1
        total_socks = trip_days + 3
        total_undergarments = trip_days + 3
    except: 
        trip_days = None
        trip_nights = None
        total_tops = None
        total_bottoms = None
        total_socks = None
        total_undergarments = None

    if depart_flight and return_flight and hotel:
       hotel.price = hotel.price * trip_days

    luggage_form = LuggageForm()

    return render(request, 'trips/detail.html', {
        'trip': trip,
        'hotel': hotel,
        'depart_flight': depart_flight, 
        'return_flight': return_flight,
        'iata': res,
        'luggage_form': luggage_form,
        'trip_days': trip_days,
        'trip_nights': trip_nights,
        'total_tops': total_tops,
        'total_bottoms': total_bottoms, 
        'total_socks': total_socks, 
        'total_undergarments': total_undergarments,
    })

def trip_list(request):
    trip = Trip.objects.filter(user=request.user)
    return render(request, 'main_app/trip_list.html', {'trip_list': trip, 'iata': res})


class TripDelete(DeleteView):
    model = Trip
    success_url = '/trips/'

class TripEdit(UpdateView):
    model = Trip
    fields = ['name', 'budget']

def SaveTrip(request):
    form = request.POST
    print(form)

def add_luggage_items(request, trip_id, airport_code):
    form = LuggageForm(request.POST)
    item = request.POST.get('item_name')
    print(item)

    if Suitcase.objects.filter(item_name=item).exists():
        print('item exists')
        return redirect('detail', trip_id = trip_id, airport_code=airport_code)
    else: 
        if form.is_valid():
            new_luggage = form.save(commit=False)
            new_luggage.user = request.user
            new_luggage.save()
            print(new_luggage)
        return redirect('detail', trip_id=trip_id, airport_code=airport_code)

def add(request, trip_id, airport_code, item_id):
    item = Suitcase.objects.get(id = item_id)
    item.quantity = item.quantity + 1
    item.save()
    return redirect('detail', trip_id=trip_id, airport_code=airport_code)

def subtract(request, trip_id, airport_code, item_id):
    item = Suitcase.objects.get(id = item_id)
    item.quantity = item.quantity - 1

    if item.quantity == 0:
        item.delete()
    else:
        item.save()
    return redirect('detail', trip_id=trip_id, airport_code=airport_code)

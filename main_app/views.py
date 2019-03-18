from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from amadeus import Client, ResponseError
from amadeus.client.decorator import Decorator
import os

from .models import Airport, Trip, Hotel, Flight

# Create your views here.
amadeus = Client(
    client_id=os.environ.get("AMADEUS_CLIENT_ID"),
    client_secret=os.environ.get("AMADEUS_CLIENT_SECRET")
)


def home(request):
    # response = amadeus.get('/v1/shopping/flight-destinations', origin='LAX')
# #     print(response.data)
#     for r in response.data:
#         a = r['price']['total']
#         a = float(a)
#         if a < 300:
#             print(
#                 f"""FROM LAX 
#                 \nDestination: {r['destination']} 
#                 \tprice: {a} 
#                 \t departure date: {r['departureDate']}
#                   \t return date: {r['returnDate']}"""
#                   )
    return render(request, 'home.html', 
    # { "flights": response.data}
    )


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
    print(request.user)

    search_list = amadeus.shopping.flight_destinations.get(
        origin=origin,
        departureDate=d_date
        ).data
    destinations = []
    # print(json.dumps(search_list.data, indent=2))
    # print(len(search_list.data))
    for destination in search_list:
    # print(json.dumps(destination, indent=2))
        d_price = float(destination['price']['total'])
        # print(d_price)
        if d_price <= budget/2:
            destinations.append(destination)
    # print(destinations)
    return render(request, 'destinations/search.html', {'destinations': destinations, 'budget': budget, 'origin': origin, 'departure_date':d_date})

def hotel_search(request, airport_code):
    budget = float(request.POST.get('budget'))
    # destination_estimate = float(request.POST.get('destination_estimate'))
    # remaining_budget = budget - destination_estimate
    hotel_search = amadeus.shopping.hotel_offers.get(cityCode=airport_code).data
# print(json.dumps(hotel_search, indent=2))
    hotels = []
    for hotel in hotel_search:
        h_price = float(hotel['offers'][0]['price']['total'])
        if h_price <= budget/3:
            hotels.append(hotel)
            
    return render(request, 'hotels/search.html', {'hotels' : hotels})

def flight_search(request, airport_code):
    budget = float(request.POST.get('budget'))
    # destination_estimate = float(request.POST.get('destination_estimate'))
    # print(destination_estimate)
    # remaining_budget = budget - destination_estimate
    origin = request.POST.get('origin')
    departure_date = request.POST.get('departure_date')

    flight_search = amadeus.shopping.flight_offers.get(destination=airport_code, origin=origin, departureDate=departure_date).data

    flights = []

    for flight in flight_search:
        n = 0
        flight['uniqueId'] = n + 1
        f_price = float(flight['offerItems'][0]['price']['total'])
        if f_price <= budget/3:
            flights.append(flight)
    
    # print(flight_search[0])

    return render(request, 'flights/search.html', {'flights': flights, 'departure_date': departure_date, 'airport_code': airport_code})

def flight_add(request):
    price = request.POST.get('flight_price')
    origin = request.POST.get('origin')
    destination = request.POST.get('destination')
    departure_date = request.POST.get('departure_date')
    return_date = request.POST.get('return_date')
    current_flight = Flight.objects.create(
        departure_date = departure_date,
        return_date = return_date,
        destination = destination,
        price = price,
        origin = origin,
        )
    print(current_flight)
    return render(request, 'trip.html', {'current_flight': current_flight})

def hotel_add(request):
    price = request.POST.get('price')
    name = request.POST.get('name')
    check_out = request.POST.get('check_out')
    check_in = request.POST.get('check_in')
    street = request.POST.get('street')
    city = request.POST.get('city')

    current_hotel = Hotel.objects.create(
        name = name,
        check_out = check_out,
        check_in = check_in, 
        address = street + city,
        price = price
        )

    print(current_hotel)
    
    return render(request, 'trip.html', {'current_hotel': current_hotel})
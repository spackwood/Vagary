from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from amadeus import Client, ResponseError
from amadeus.client.decorator import Decorator
import os
# Create your views here.
amadeus = Client(
    client_id=os.environ.get("AMADEUS_CLIENT_ID"),
    client_secret=os.environ.get("AMADEUS_CLIENT_SECRET")
)


def home(request):
    response = amadeus.get('/v1/shopping/flight-destinations', origin='LAX')
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
    return render(request, 'home.html', { "flights": response.data})


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

    print(destinations)
    return render(request, 'destinations/search.html', {'destinations': destinations, 'budget': budget})

def hotel_search(request, airport_code):
    budget = float(request.POST.get('budget'))
    flight_price = float(request.POST.get('flight_price'))
    remaining_budget = budget - flight_price
    hotel_search = amadeus.shopping.hotel_offers.get(cityCode=airport_code).data
# print(json.dumps(hotel_search, indent=2))
    hotels = []
    for hotel in hotel_search:
        h_price = float(hotel['offers'][0]['price']['total'])
        if h_price <= remaining_budget:
            hotels.append(hotel)
            
    return render(request, 'hotels/search.html', {'hotels' : hotels, 'remaining_budget': remaining_budget})
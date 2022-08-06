#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data = DataManager()
flight_search = FlightSearch()
notifications = NotificationManager()

sheet_data = data.prices
sheet_users = data.user_list

for item in sheet_data:
    city = item["city"]
    object_id = item["id"]
    iata = flight_search.fetch_iata(city)
    flight_data = flight_search.search_flight(iata)
    
    if flight_data == None:
        flight_data = flight_search.search_flight(iata, stopovers=1)
    
    try:
        price = flight_data.price
    except AttributeError:
        price = 0
        
    if item["lowestPrice"] > price and price != 0:
        notifications.send_message(flight_data)
        for user in sheet_users:
            notifications.send_email(flight_data, user["email"])
        
    
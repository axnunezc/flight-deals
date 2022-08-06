from decouple import config
import requests
from datetime import datetime, timedelta
from flight_data import FlightData

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.API_KEY = config("API_KEY")
        self.LOCATION_SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
        self.FLIGHT_SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
        self.search_headers = {
            "apikey": self.API_KEY
        }
    
    def fetch_iata(self, city):
        search_params = {
            "term": city,
            "location_types": "city"
        }
        
        response = requests.get(url=self.LOCATION_SEARCH_ENDPOINT, params=search_params, headers=self.search_headers)
        location_data = response.json()["locations"]
        code = location_data[0]["code"]
        return code
    
    def search_flight(self, city_code, stopovers=0):
        start_search = datetime.today() + timedelta(days=1)
        end_search = datetime.today() + timedelta(days=6*30)

        formatted_from_date = start_search.strftime("%d/%m/%Y")
        formatted_to_date = end_search.strftime("%d/%m/%Y")
        
        flight_search_params = {
            "fly_from": "LON",
            "fly_to": city_code,
            "date_from": formatted_from_date,
            "date_to": formatted_to_date,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "max_stopovers": stopovers,
            "one_for_city": 1,
            "curr": "USD"
        }
        
        response = requests.get(url=self.FLIGHT_SEARCH_ENDPOINT, params=flight_search_params, headers=self.search_headers)
        
        try:
            data = response.json()["data"][0]    
        except IndexError:
            return None
        
        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        
        if stopovers > 0:
            flight_data.destination_city = data["route"][1]["cityTo"]
            flight_data.destination_airport=data["route"][1]["flyTo"]
            flight_data.stop_overs = stopovers
            flight_data.via_city = data["route"][0]["cityTo"]
        
        return flight_data
        
        
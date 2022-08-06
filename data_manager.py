import requests
from decouple import config

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.SHEETS_ENDPOINT = "https://api.sheety.co/e05bcfe8bb626a28a52f03b41af4c96a/flightDeals/prices"
        self.SHEETS_USERS_ENDPOINT = "https://api.sheety.co/e05bcfe8bb626a28a52f03b41af4c96a/flightDeals/users"
        self.TOKEN = config("TOKEN")
    
        self.sheets_headers = {
            "Authorization": f"Bearer {self.TOKEN}"
        }
        
        self.response = requests.get(self.SHEETS_ENDPOINT, headers=self.sheets_headers)
        self.prices = self.response.json()["prices"]
        
        self.users = requests.get(self.SHEETS_USERS_ENDPOINT, headers=self.sheets_headers)
        self.user_list = self.users.json()["users"]
        
    def update_iata(self, object_id, city_code):
        object_endpoint = f"{self.SHEETS_ENDPOINT}/{object_id}"
        
        update_params = {
            "price": {
                "iataCode": city_code
            }
        }
        
        update = requests.put(object_endpoint, json=update_params, headers=self.sheets_headers)
        print(update.status_code)

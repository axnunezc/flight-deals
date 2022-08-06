from twilio.rest import Client
from decouple import config
import smtplib

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.acc_sid = config("ACC_SID")
        self.auth_token = config("AUTH_TOKEN")
        self.email = config("EMAIL")
        self.password = config("PASSWORD")
        
        self.client = Client(self.acc_sid, self.auth_token)
        
    def send_message(self, flight_data):
        if flight_data.stop_overs > 0:
            message = self.client.messages \
                    .create(
                        body=f"Low price alert! \nOnly ${flight_data.price} to fly from {flight_data.origin_city}-{flight_data.origin_airport} to {flight_data.destination_city}-{flight_data.destination_airport}, from {flight_data.out_date} to {flight_data.return_date} \n \nFlight has {flight_data.stop_overs} stop over(s), via {flight_data.via_city}",
                        from_="+17406854152",
                        to="+15748559504"
                    )
            print(message.status)
        else:
            message = self.client.messages \
                        .create(
                            body=f"Low price alert! \nOnly ${flight_data.price} to fly from {flight_data.origin_city}-{flight_data.origin_airport} to {flight_data.destination_city}-{flight_data.destination_airport}, from {flight_data.out_date} to {flight_data.return_date}",
                            from_="+17406854152",
                            to="+15748559504"
                        )
            print(message.status)
            
    def send_email(self, flight_data, to_email):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.password)
            connection.sendmail(from_addr=self.email, to_addrs=to_email, msg=f"Subject:Flight Deal\n\nLow price alert! \nOnly ${flight_data.price} to fly from {flight_data.origin_city}-{flight_data.origin_airport} to {flight_data.destination_city}-{flight_data.destination_airport}, from {flight_data.out_date} to {flight_data.return_date}\nhttps://www.google.co.uk/flights?hl=en#flt={flight_data.origin_airport}.{flight_data.destination_airport}.{flight_data.out_date}*{flight_data.destination_airport}.{flight_data.origin_airport}.{flight_data.return_date}")
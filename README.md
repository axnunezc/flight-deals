# flight-deals
This script uses the Flight Search API to find deals on flights to a list of destinations provided in a Google Sheets page. The API then checks the current price for a ticket and, if it is lower than the previously recorded lowest price, sends the user an SMS using the Twilio API and an email using the SMTPLib library.

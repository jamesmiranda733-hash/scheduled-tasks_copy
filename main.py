import requests
from twilio.rest import Client
import smtplib
import os
from email.message import EmailMessage

app_password_2 = os.environ["APP_PASSWORD_2"]
my_gmail = os.environ["MY_EMAIL"]
account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]
weather_api_key = os.environ["WEATHER_API_KEY"]
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
LINK = "https://forecast.weather.gov/MapClick.php?lat=35.2133&lon=-101.8327"

weather_parameters = {
    "lat": 35.2220,
    "lon": -101.8313,
    "appid": weather_api_key,
    "cnt" : 4
}

response = requests.get(OWM_ENDPOINT, params=weather_parameters)
response.raise_for_status()
weather_data = response.json()
weather_data = weather_data["list"]
will_rain = False

for hour_data in weather_data:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
        break

if will_rain:
    subject = "🌧️ Weather Alert — Rain Expected"
    body = (
        "Good morning!\n\n"
        "Based on the latest weather forecast, rain may "
        "occur later today.\n\n"
        "Remember to bring an umbrella or a raincoat "
        "before heading out.\n\n"
        "Stay safe and have a wonderful day!\n\n"
        f"View Live Forecast: {LINK}")
    )

else:
    subject = "☀️ Weather Update — No Rain Expected"
    body = (
        "Good morning!\n\n"
        "Based on the latest weather forecast, no rain "
        "is expected during the forecast period.\n\n"
        "You should be good to head out without "
        "an umbrella.\n\n"
        "Enjoy your day!\n\n"
        f"View Live Forecast: {LINK}")
    )

with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    connection.starttls()
    connection.login(user=my_gmail, password=app_password)

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = my_gmail
    message["To"] = my_gmail
    message.set_content(body)

    connection.send_message(message)

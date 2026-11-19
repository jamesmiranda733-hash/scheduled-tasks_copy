import requests
from twilio.rest import Client
import smtplib
import os



app_password_2 = os.environ["APP_PASSWORD_2"]
my_gmail = os.environ["MY_EMAIL"]
account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]
weather_api_key = os.environ["WEATHER_API_KEY"]
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

weather_parameters = {
    "lat": 16.5691,
    "lon": -88.5276,
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

if will_rain:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_gmail, password=app_password)
        connection.sendmail(
            from_addr=my_gmail,
            to_addrs=my_gmail,
            msg= f"Subject: TODAY IS GOING TO BE VERY RAINY! \n\n"
            "Rain is expected throughout the day today, "
                 "so make sure to plan ahead and be prepared for wet weather. "
                 "Be sure to bring an umbrella or rain jacket before heading out to avoid "
                 "getting caught in the rain. Roads and sidewalks may become slippery, "
                 "so take extra precautions while traveling. "
                 "Stay safe, stay dry, and don't forget your umbrella!"
        )
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="sms_2fa",
        to = "+18068477492",
         from_ = "+17372583478",)
    print(message.status)





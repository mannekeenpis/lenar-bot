import schedule
import time


# Remember to bring an umbrella
def send_message():
    weather_params = {
        "lat": 55.764898,
        "lon": 52.455413,
        "appid": api_key,
        "exclude": "current, minutely, daily"
    }

    response = requests.get(OWM_Endpoint, params=weather_params)
    response.raise_for_status()
    weather_data = response.json()
    weather_slice = weather_data["hourly"][:12]

    will_rain = False

    for hour_data in weather_slice:
        condition_code = hour_data["weather"][0]["id"]
        if int(condition_code) < 700:
            will_rain = True

    if will_rain:
        bot.send_message(914025175, "It's going to rain today. Remember to bring an ☔️")


schedule.every().day.at("11:42").do(send_message)

while True:
    schedule.run_pending()
    time.sleep(1)
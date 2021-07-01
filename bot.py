from telebot import types
from datetime import datetime
import sqlite3
import time
import urllib
import config
import telebot
import requests
import schedule

connect = sqlite3.connect('database.db')

cursor = connect.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS visit(
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id integer,
    date date,
    time text
    )
""")

connect.commit()
connect.close()

# Bot token
bot = telebot.TeleBot(config.token)

# Weather api
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = "8f14ac1ce7426fef035aa2a985c43017"

# Coordinates for ISS
MY_LAT = 55.764898
MY_LONG = 52.455413


@bot.message_handler(regexp='space')
def reply_space(message):
    url = 'https://apod.nasa.gov/apod/fap/image/2003/AndromedaStation.jpg'
    f = open('out.jpg', 'wb')
    f.write(urllib.request.urlopen(url).read())

    bot.send_photo(message.chat.id, open('out.jpg', 'rb'))


@bot.message_handler(regexp='virus')
def reply_virus(message):
    sticker_id = "CAACAgIAAxkBAAI3hV56HntGyLflxiv_AAGF1D6FOAABcbcAAi8AA-EwpinqvCmfV2_7GxgE"
    bot.send_sticker(message.chat.id, sticker_id)


@bot.message_handler(regexp='guido')
def reply_guido(message):
    sticker_id = "CAACAgIAAxkBAAI4il58xyJdfRRqZRj0sQnmAAEcZ64_-gACHwADMPLlD7MzuT5hmEqJGAQ"
    bot.send_sticker(message.chat.id, sticker_id)


@bot.message_handler(commands=['start'])
def say_hello(message):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    user_id = message.from_user.id

    last_visits = cursor.execute("""
        SELECT *
        FROM visit
        WHERE user_id = (?)
        ORDER BY id DESC
    """, [user_id]).fetchall()

    if len(last_visits) != 0:
        reply_text = f"Hey! Last time you came in {last_visits[0][2]}"
    else:
        reply_text = 'Hello new user!'
    time = datetime.datetime.now()
    date = datetime.date.today()

    cursor.execute("""
        INSERT INTO visit (user_id, date)
        VALUES (?, ?)
    """, [user_id, time])

    connect.commit()
    connect.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('/start')
    btn2 = types.KeyboardButton('/valute')
    btn3 = types.KeyboardButton('/randomText')
    btn4 = types.KeyboardButton('/weather')

    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, reply_text, reply_markup=markup)


@bot.message_handler(commands=['randomText'])
def printRandomText(message):
    bot.send_message(message.chat.id, "This text is random. Trust me.")


@bot.message_handler(commands=['valute'])
def get_valute(message):
    data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    usd = data['Valute']['USD']['Value']
    eur = data['Valute']['EUR']['Value']
    gbp = data['Valute']['GBP']['Value']

    bot.send_message(message.chat.id, f"USD = {usd}, EUR = {eur}, GBP = {gbp}")


@bot.message_handler(commands=['weather'])
def send_start(message):
    msg = bot.send_message(message.chat.id, "Enter your city")

    bot.register_next_step_handler(msg, city_choose)


def city_choose(message):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={message.text},ru&APPID=3c476f22a5b257b9d84b96dbf18ad854'

    response = requests.get(url).json()

    bot.send_message(message.chat.id,
                     f"The city {message.text} is now approximately {int(response['main']['temp'] - 273.15)} degrees")


@bot.message_handler(regexp='hello')
def reply_to_hello(message):
    bot.send_message(message.chat.id, f"O, hello, {message.from_user.first_name}! I know you!")


@bot.message_handler(content_types=['text'])
def reply_to_text(message):
    text = message.text
    bot.send_message(message.chat.id, f"You wrote {text}, I am not yet able to process such a command")


# ISS overhead
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(59)
    if is_iss_overhead() and is_night():
        bot.send_message(914025175, "Look Up👆\n\nThe ISS 🛰 is above you in the sky.️")


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


bot.polling()

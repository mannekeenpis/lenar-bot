import telebot
import requests
from telebot import types
import sqlite3
import datetime
import urllib
import config

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

token = "1147601760:AAF6BYCUoxtvZ7kpKHC5afICffzwa8cCS9U"

bot = telebot.TeleBot(token)

@bot.message_handler(regexp='космос')
def reply_space(message):
    url = 'https://apod.nasa.gov/apod/image/2003/BhShredder_NASA_1080.jpg'
    f = open('out.jpg','wb')
    f.write(urllib.request.urlopen(url).read())

    bot.send_photo(message.chat.id, open('out.jpg', 'rb'))   


@bot.message_handler(regexp='карантин')
def reply_virus(message):
    sticker_id = "CAACAgIAAxkBAAI3hV56HntGyLflxiv_AAGF1D6FOAABcbcAAi8AA-EwpinqvCmfV2_7GxgE"
    bot.send_sticker(message.chat.id, sticker_id)

@bot.message_handler(regexp='гвидо')
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
        reply_text = f"Привет! Последний раз вы заходили {last_visits[0][2]}"
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

    markup.add(btn1, btn2, btn3)

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
     msg = bot.send_message(message.chat.id, "Введите, пожалуйста, город")    

     bot.register_next_step_handler(msg, city_choose)

 def city_choose(message):
     url = f'http://api.openweathermap.org/data/2.5/weather?q={message.text},ru&APPID=3c476f22a5b257b9d84b96dbf18ad854'

     response = requests.get(url).json()

     bot.send_message(message.chat.id, f"В городе {message.text} сейчас примерно {int(response['main']['temp'] - 273.15)} градусов")  


@bot.message_handler(regexp='привет')
def reply_to_hello(message):
    bot.send_message(message.chat.id, f"О, привет, {message.from_user.first_name}! А я тебя знаю!")

@bot.message_handler(content_types=['text'])
def reply_to_text(message):
    text = message.text
    bot.send_message(message.chat.id, f"Вы написали {text}, я пока не умею обрабатывать такую команду")


bot.polling()
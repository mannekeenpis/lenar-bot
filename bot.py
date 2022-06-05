import time
import os
import requests
import telebot
import pandas
import feedparser
import random
import schedule

from flask import Flask, request
from datetime import datetime
from time import mktime
from multiprocessing import *
from telebot import types

TOKEN = os.environ['BOT_API_TOKEN']
bot = telebot.TeleBot(TOKEN)
APP_URL = f'https://lenar-technopolis-bot.herokuapp.com/{TOKEN}'
server = Flask(__name__)


# It's going to rain today
def start_process():
    p1 = Process(target=TimeSchedule.start_schedule, args=()).start()


class TimeSchedule():
    def start_schedule():
        schedule.every().day.at("03:00").do(TimeSchedule.rain_today)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def rain_today():
        OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
        api_key = os.environ.get('API_KEY')

        weather_params = {
            "lat": 55.766334,
            "lon": 52.460639,
            "appid": api_key,
            "exclude": "current,minutely,daily"
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
            my_id = os.environ.get('MY_ID')
            bot.send_message(chat_id=my_id, text="It's going to rain today. Remember to bring an ☔")


# Voice
@bot.message_handler(content_types=["voice"])
def reply_media(message):
    random_media = [
        'CAACAgIAAxkBAAEE3mxik3DNbfJsz7CWT4Iaj7FFxUji-wAC8gEAAvnkbAABFGZP0PSik3UkBA',
        'CAACAgIAAxkBAAEE3mRik3AcS06Fv0AFlIOH1A66xN0qhgACfQIAAvnkbAABcAABA648YQ08JAQ',
        'CAACAgIAAxkBAAEE3cVik0Ap8f_x294skvy7ZciKlDuDYgAC1wEAAvnkbAAB4w5wG9hf2x0kBA',
        'CAACAgIAAxkBAAEE3ZNikzrWRCP-cQUE39rX0uf_mx0zZQAC8AIAAuPwEwxu6MM3_45aHSQE',
        'CAACAgIAAxkBAAEE3Ytikzq5UWWyBKX2MntRwM_JoasQdAAC7wIAAuPwEwz4T_0I0SlcoCQE',
        'CAACAgIAAxkBAAEE3Y1ikzq--tE7GVNUHuJ2e9LJCaBhcwAC7gIAAuPwEwy9WhQtdjXq0iQE',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_media), reply_to_message_id=message.message_id)


# Images
@bot.message_handler(content_types=["pinned_message", "photo", "video"])
def reply_media(message):
    random_media = [
        'CAACAgIAAxkBAAEE3YVikzjVMsAjk5qIlnGuuexQRmBjcAACywIAAuPwEwzCNDIGj1-bgiQE',
        'CAACAgIAAxkBAAEE3ZFikzrJ3-eMnA1vTANhPMn_vYXRsgAC6gIAAuPwEwzU9W4mQkSiPyQE'
        'CAACAgIAAxkBAAEE3kZik2zzhUB72SIqpFSvSstpTD1eOQAChBYAAicD6UtWHCmJUsvcXyQE',
        'CAACAgIAAxkBAAEE3khik2z1ZA-1sbe8n3uRujmv2vo2RQAC2RgAAiud6EuyXNu_8FbRLCQE',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_media), reply_to_message_id=message.message_id)


# Money
@bot.message_handler(regexp='деньги')
def reply_money(message):
    random_money = [
        'CAACAgIAAxkBAAEE3b1ikz89DFS4NHTWfVl9xbOvujWWWAACygEAAvnkbAABUX95-rGy7bwkBA',
        'CAACAgIAAxkBAAEE3ZtikzxnPDcqy09BvcCwcdiZR599sQACnQEAAvnkbAABG-jcw1OqPrAkBA',
        'CAACAgIAAxkBAAEE3ZlikzxksdK2TSwKhfcx7R8t-fijewACnwEAAvnkbAABOocVUNm4nIYkBA',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_money), reply_to_message_id=message.message_id)


# Books
@bot.message_handler(regexp='книга|книги|книге|книгу|книжка|книжке|книг|книгам|книгой|книгою|книгами|книгах|читал|читаю|'
                            'прочитал|читать|прочитаю|прочитаешь')
def reply_books(message):
    book_message = [
        'CAACAgIAAxkBAAEE3olik3UvKZglEXLEGI-UX0mBOCMYlQACnQgAAgk7OxNbbX7w-QABQ2okBA',
    ]
    bot.send_sticker(message.chat.id, random.choice(book_message), reply_to_message_id=message.message_id)


# Name
@bot.message_handler(regexp='Ленар|ленар|Ленару|ленару|Ленара|ленара')
def reply_name(message):
    random_lenar = [
        'CAACAgIAAxkBAAEE3lpik29rGqz8Uir-MuPE7y3epc2QZwAChQIAAvnkbAABmd-cqFz6D9skBA',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_lenar), reply_to_message_id=message.message_id)


# Jagermaister
@bot.message_handler(regexp='jagermeister|Jagermeister|ягер|Ягермейстер|ягермастер|Ягермастер|бугульма|Бугульма|'
                            'бугульму|Бугульму|бугульме|Бугульме')
def reply_jagermeister(message):
    random_jagermeister = [
        'CAACAgIAAxkBAAEE3kpik2z5eXWRb0ZHAtfB3-F6-fIo2AAChxsAAvaD6UukzGHH1sJdkCQE',
        'CAACAgQAAxkBAAEEkHViZ-i71shmzuKhQt_lybq8OE2xJgACChgAAoB5FQABh6BS2WdOJRMkBA',
        'CAACAgQAAxkBAAEEkHdiZ-jDg2NP5r5oSsOhPtIQjSCo7wACgCIAAoB5FQAB5h5pXsvyTzAkBA',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_jagermeister), reply_to_message_id=message.message_id)


# Goodbye
@bot.message_handler(regexp='пока|Пока|счастливо|Счастливо|до свидания|До свидания|гудбай|Гудбай')
def reply_goodbye(message):
    random_goodbye = [
        'CAACAgIAAxkBAAEE3kRik2yPu0VCsYNI_NkyiDu7J9N-yQACcxwAAhmc8Uv2ZviUNs8wmyQE',
        'CAACAgIAAxkBAAEE3c1ik0DkH4nBnKmRdNoQEqK0aoKkhgAC8gEAAvnkbAABFGZP0PSik3UkBA',
        'CAACAgIAAxkBAAEE3a1ikz3-5-SU1BcB-N-t3k8H74UPawACwQEAAvnkbAAB-0l-qmLr2hQkBA',
        'CAACAgIAAxkBAAEE3Xlikzdq7FT2WeRZ5a-RDzJVmGUbEwACcxwAAhmc8Uv2ZviUNs8wmyQE',
        'CAACAgIAAxkBAAEEk-tiajna9nd6_rTv7gMbihx3Uq-VYwACJAAD5HgnCHFqpc1JBgztJAQ',
        'CAACAgQAAxkBAAEEkHdiZ-jDg2NP5r5oSsOhPtIQjSCo7wACgCIAAoB5FQAB5h5pXsvyTzAkBA',
        'CAACAgIAAxkBAAEEk_9iajoaUZfjm1iUxICWAtkKNyvlpgACNwAD5HgnCNceUNQRYMVbJAQ',
        'CAACAgIAAxkBAAEElA9iajpKMBTE1OVGxnWzSem8vNR8MgACPgAD5HgnCIfBIUQ6SiLxJAQ',
        'CAACAgIAAxkBAAEEk8Viajk1Dw6sA45PDKzD4mTt8Nd8MQACBgAD5HgnCCY9zhXrehdnJAQ',
        'CAACAgIAAxkBAAEEk8liajlGET_w-MhnUzNJxU6H5SCLAgACCQAD5HgnCLmiHXnNttUGJAQ',
        'CAACAgIAAxkBAAEEk9Viajl3br6Vw89yk-1_7JbuvFuBjAACEwAD5HgnCMOTOibG3vCvJAQ',
        'CAACAgIAAxkBAAEElIZiam4W1sOSBcB9M6LyCe3IDeVViwACcwMAAvnkbAABicHsqQgiHWskBA',
        'CAACAgIAAxkBAAEElIhiam5QlaviZJLoF0urswqTyPAJmwACkgMAAvnkbAABKDGVARsLiUUkBA',
        'CAACAgIAAxkBAAEElJxiam89bpqqtPjrWZuk9CG_mJ1AiQACgwEAAvnkbAABaeDcFvmy5BskBA',
        'CAACAgIAAxkBAAEElKZiam-PAAEfG0qhd8ntvZndLQABezkMAAJqAQAC-eRsAAGINwNAUIS5eCQE',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_goodbye), reply_to_message_id=message.message_id)


# Music
@bot.message_handler(regexp='soundcloud|mixcloud|bandcamp|music.yandex|spotify')
def reply_music(message):
    random_music = [
        'CAACAgIAAxkBAAEE3lhik25eU-4OUkQ1PqbMKzT0mUT-sAACjQIAAvnkbAABhvhSvFt-KPwkBA',
        'CAACAgIAAxkBAAEE3dlik0GUUJAg54gcTyoNV6XiNpe0_AACAQIAAvnkbAABgYkUR2jzKikkBA',
        'CAACAgIAAxkBAAEE3d1ik0GaD--dbZjsWRR31iSSIEImyQAC9AEAAvnkbAABNUT2vUtCTSYkBA',
        'CAACAgIAAxkBAAEE3YFikzhnlb6XZoRsuz6seBUnyi4MfQAC1gEAAvnkbAABHxVe-cb2qsMkBA',
        'CAACAgIAAxkBAAEEkAZiZ-YjjKm7uM7RdopsPSAg5ssz4wACCwgAAtjY4QABFh1qAzD5_yIkBA',
        'CAACAgIAAxkBAAEEkApiZ-Yp3guu20ZaEIzAx-ahx9L2agACCQgAAtjY4QAB2MGWR-YJWX8kBA',
        'CAACAgIAAxkBAAEEkBJiZ-ZzHOcykEtRtKLzWS_1ixmARwAC8gYAAipVGAJs9kVePXd9QiQE'
        'CAACAgIAAxkBAAEEkBhiZ-aVGIHc7UggCU2zXdZd9gRBjwAClgcAAipVGAKLbGVlcW-KJCQE',
        'CAACAgIAAxkBAAEEkB5iZ-az0RWtf1Dr1PUbboubpZPtUAACpgcAAipVGAI8YM5IdqLVmiQE',
        'CAACAgIAAxkBAAEEkCBiZ-bALpNV82CUE2eReJ82th7ccQACpwcAAipVGALmPLdeC1cpoCQE',
        'CAACAgIAAxkBAAEEkDRiZ-dDz-6f_pcoY0ZZSLMEueIsSgACSwADTMV6AAH4TRm1eEJn1SQE',
        'CAACAgIAAxkBAAEElKJiam901FOEUe_X12ueMTXoDKf_vAACZgEAAvnkbAABoX7P-WT-negkBA',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_music), reply_to_message_id=message.message_id)


# Work
@bot.message_handler(regexp='работа|Работа|работе|Работе|работу|Работу|работал')
def reply_work(message):
    random_work = [
        'CAACAgIAAxkBAAEE3ZVikzvn9GPs2hoU1RtndeDYPkpRVQACxQIAAuPwEwyPxIgt60w_2CQE',
        'CAACAgIAAxkBAAEEkJJiZ-lqARD-HTyAKV69bT2aNONy3wACFwADa2iODlABCx8udmkJJAQ',
        'CAACAgIAAxkBAAEEkDpiZ-dh3REiA8tLE1M9bRJm3kxuGgACjgcAAipVGALgmThJQPq0oCQE',
        'CAACAgIAAxkBAAEEkF5iZ-g7NgjReB-pfPZJBOG8So7nBQACTgADNIWFDBPjZk_lcIiMJAQ'
        'CAACAgIAAxkBAAEEkGBiZ-g9UajOz0hcUEa_Ix51Ll_E3AACTAADNIWFDIu0XT3iVwhiJAQ',
        'CAACAgIAAxkBAAEEkGJiZ-hBgniPssvGssDxhn6b6YUkRgACSgADNIWFDONV4SOdcxKqJAQ',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_work), reply_to_message_id=message.message_id)


# Yes
@bot.message_handler(regexp='конечно|Конечно|разумеется|Разумеется|так и есть|Так и есть|давай|Давай|да')
def reply_yes(message):
    random_yes = [
        'CAACAgIAAxkBAAEE3odik3UpG0D2Ww_Vgtz2B3wQhSePswACmQgAAgk7OxNRVRJoMqOh8SQE',
        'CAACAgIAAxkBAAEE3k5ik20AAVneTU4ojKWa4LXzFA_VaksAAnACAAL55GwAAfaA4kSD3N8jJAQ',
        'CAACAgIAAxkBAAEE3d9ik0HjMvemlJM51y2B3Avx3tb8-AACdQIAAvnkbAAB8erfWz9rKMQkBA',
        'CAACAgIAAxkBAAEE3cNik0AlPbIHVzXF86krocOB8rKddAAC2gEAAvnkbAABmnQw-PbzfWIkBA',
        'CAACAgIAAxkBAAEE3cdik0AtKrE5nfsL7viG8t3u7PiaCwAC0wEAAvnkbAABaWEhvNEK5wgkBA',
        'CAACAgIAAxkBAAEE3clik0AxXii_1x66hDGpk-dYdUa7QgAC0gEAAvnkbAABATzAWw7Er68kBA',
        'CAACAgIAAxkBAAEE3aVikz1xLmG2JYQp-1qyotYM-YPw3QACsQEAAvnkbAAB92nYTHz9cOUkBA',
        'CAACAgIAAxkBAAEE3aNikz1uJuJe2-mNYkD0O0ih1hMblAACswEAAvnkbAABWBWJ_Xv3Y1EkBA',
        'CAACAgIAAxkBAAEEkFRiZ-gKQ_FxjPSn-7xR92uNUBpYsQACYwADNIWFDOVRjVkiEKL6JAQ',
        'CAACAgIAAxkBAAEEkFZiZ-gOnBiidZ-h8lXSgD5yJggqPwACYgADNIWFDF3nYiwS_GAoJAQ',
        'CAACAgIAAxkBAAEEk8diajk8Krbu5aFPBdwxSsTZW_TLggACBwAD5HgnCIEmQYo-_P9-JAQ',
        'CAACAgIAAxkBAAEEk_tiajoO4IokPFLB3UPHQgjV_LifRAACNAAD5HgnCPhcQpFrnQ33JAQ',
        'CAACAgIAAxkBAAEEk-Viajm4GCQU4fuOVgtegLLzI7hk7wACHQAD5HgnCCdgBLMLh8bbJAQ',
        'CAACAgIAAxkBAAEElIpiam6ow4744EYWtxW7AUFfNcOoQQACDAEAAvnkbAABXarqC6W7iY4kBA',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_yes), reply_to_message_id=message.message_id)


# How
@bot.message_handler(regexp='сколько|Сколько|за сколько|За сколько|почём|Почём|цена|Цена')
def reply_how(message):
    random_how = [
        'CAACAgIAAxkBAAEEk8Niajkvh9lVL1Lj04uRM8dDbQut_wACBQAD5HgnCIK0XZnqowrBJAQ',
        'CAACAgIAAxkBAAEElJBiam7wgG_HhG2a3BuiAmAJNEbSjwACMQEAAvnkbAABgLXj9HvptQ4kBA',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_how), reply_to_message_id=message.message_id)


# Цыгане
@bot.message_handler(regexp='цыган|Цыган|цыгане|Цыгане|цыгану|Цыгану')
def reply_gypsies(message):
    random_gypsies = [
        'CAACAgIAAxkBAAEElIJiam37yW5XiGCHxkp9RLfI_mArhwACpgMAAvnkbAABf6BYa_P6Cw0kBA',
        'CAACAgIAAxkBAAEElIRiam4AAZkTl3VSz5bNDDcq5VatlUYAAuMDAAL55GwAAdJPlFzXDaRZJAQ',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_gypsies), reply_to_message_id=message.message_id)


# Где
@bot.message_handler(regexp='где|Где')
def reply_where(message):
    random_where = [
        'CAACAgIAAxkBAAEElIxiam7kxIwDHHvHSdx8Ytqm7QaR0gACLQEAAvnkbAABdIcfl9yS1D0kBA',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_where), reply_to_message_id=message.message_id)


# Мат
@bot.message_handler(regexp='мат|Мат|матерись|Матерись|материшься|Материшься|матреится|Матерится|матерюсь|Матерюсь'
                            '|матерился|Матерился')
def reply_swearing(message):
    random_swearing = [
        'CAACAgIAAxkBAAEE3a9ikz4BJKcmoeV3NeIQpQPXNK2aOQACwAEAAvnkbAABoDH6R5pwO0ckBA',
        'CAACAgIAAxkBAAEElJRiam8U47hz9GnlOyXTQbRMYWGVUgACPwEAAvnkbAABg86slV92oGokBA',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_swearing), reply_to_message_id=message.message_id)


# Ебать мозг
@bot.message_handler(regexp='мозг|Мозг|мозги|Мозги|мозгоеб|Мозгоеб|мозгоёб|Мозгоёб')
def reply_brain(message):
    random_brain = [
        'CAACAgIAAxkBAAEElJZiam8hZ8GXPydcK91fwmO0CU-PaQACQwEAAvnkbAAByXmvNTlo7TskBA',
        'CAACAgIAAxkBAAEE3Z1ikz0GBNCC1VhJxt2FhnXL7I_6qgACoQEAAvnkbAAByh-RX6CzXvgkBA'
    ]
    bot.send_sticker(message.chat.id, random.choice(random_brain), reply_to_message_id=message.message_id)


# Know
@bot.message_handler(regexp='знаю|Знаю|знай|Знай|знал|Знал|знает|Знает|знать|Знать')
def reply_know(message):
    random_know = [
        'CAACAgIAAxkBAAEE3pNik3aEK-wbF90FDpkeMHlx4cP8fQACmggAAgk7OxM6MEYpohw-JSQE',
        'CAACAgIAAxkBAAEE3pFik3ZZXAld_7t6R9IC-XdfDI57IgACnggAAgk7OxNY9OSgkAXRqSQE',
        'CAACAgIAAxkBAAEE3o9ik3Y288FaqQ-Jir3Dv62LRaSIsAACpQgAAgk7OxODgKumZXRqASQE',
        'CAACAgIAAxkBAAEE3lxik29uozdiDeasS1wXA0ZTO8otJQAChAIAAvnkbAABR-gwu4XLxqYkBA',
        'CAACAgIAAxkBAAEElJhiam8oLObBx2Vk799D_9qr4lN5QgACRAEAAvnkbAABY8YI7nUWLKwkBA',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_know), reply_to_message_id=message.message_id)


# Cool
@bot.message_handler(regexp='было|Было')
def reply_cool(message):
    random_cool = [
        'CAACAgIAAxkBAAEElKxiam-ssls1Ig8K55dhHSqJp80n0AACfgEAAvnkbAABwChVPeOaNTgkBA',
        'CAACAgIAAxkBAAEE3aVikz1xLmG2JYQp-1qyotYM-YPw3QACsQEAAvnkbAAB92nYTHz9cOUkBA',
        'CAACAgIAAxkBAAEE3aNikz1uJuJe2-mNYkD0O0ih1hMblAACswEAAvnkbAABWBWJ_Xv3Y1EkBA',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_cool), reply_to_message_id=message.message_id)


# Watch
@bot.message_handler(regexp='youtu.be|youtube|zen.yandex|instagram')
def reply_watch(message):
    random_watch = [
        'CAACAgIAAxkBAAEE3otik3U6Bqpf8A8rzufQrxLABB8__gACqAgAAgk7OxOGkHZbEt8dQSQE',
        'CAACAgIAAxkBAAEE3o1ik3VA4A4U9clIfy0ghV3yv8naRAACpwgAAgk7OxMbqdsXc_sEyiQE',
        'CAACAgIAAxkBAAEElKBiam9JklQ19RvO_hfIuCgqbecciQACTQEAAvnkbAABJa0X7MzmAqskBA',
        'CAACAgIAAxkBAAEE3adikz10QvZQGOwCQsxuMMDye2fOxAACrwEAAvnkbAABNO4CCT7bqPgkBA',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_watch), reply_to_message_id=message.message_id)


# Fail
@bot.message_handler(regexp='пиздец|Пиздец|провал|Провал|отказ|Отказ|фэйл|Фэйл|наебали|Наебали|наебал|Наебал|обманули|'
                            'Обманули|кинули|Кинули|кинул|Кинул')
def reply_fail(message):
    random_fail = [
        'CAACAgIAAxkBAAEE3kxik2z8148z-iAQF2CXyruWgNVMTgACUhcAAuPw6EuIv1TXwJuN2CQE',
        'CAACAgIAAxkBAAEE3dtik0GXYOVVeXyANQdKnPZ_HuNcBwAC-AEAAvnkbAABxirfsMQfRNIkBA',
        'CAACAgIAAxkBAAEE3ctik0DiXJPCTv1T0KdXUkAjifvaIwAC8wEAAvnkbAABhaKTMhDqj60kBA',
        'CAACAgIAAxkBAAEE3dFik0DqzsOENgJ6RS93WAl-C-jXAAPoAQAC-eRsAAEgaFJYwYUboyQE',
        'CAACAgIAAxkBAAEE3dNik0DwQBm4krEAARhEENm5pr1FQEsAAukBAAL55GwAAekhLzAEF0ZwJAQ',
        'CAACAgIAAxkBAAEE3bVikz8xKs6Yt_ykMWRcgR9ZO9Av8wAC0AEAAvnkbAAB9ZvynKLhv7QkBA',
        'CAACAgIAAxkBAAEE3X1ikzguIrfqwWqacAyt2aAtTX66QgACuwIAAuPwEwwS3zJY4LIw9CQE',
        'CAACAgIAAxkBAAEEkExiZ-f2A4yWAkfNCXwcAAH23o5lOtMAAmkAAzSFhQxCh-za-DCcHyQE',
        'CAACAgIAAxkBAAEEkE5iZ-f9bCT0ks9viu1wJg1oeHYyMAACbQADNIWFDDbkiAZrREh_JAQ',
        'CAACAgIAAxkBAAEEkFJiZ-gDlCXpyxkHuajfa1-0KlI2uQACZgADNIWFDHy3R6whcWViJAQ',
        'CAACAgIAAxkBAAEEkGZiZ-hQ3hy9jTguga5ZGOa-P1LcBAACQwADNIWFDKkJFPJdnMYjJAQ',
        'CAACAgIAAxkBAAEEkGpiZ-h77eGPt7BSQUdsEJDJONuDMAACLQADNIWFDGiid5vEFNojJAQ',
        'CAACAgIAAxkBAAEElKRiam-BijvR64PLbV3VEPwIFb5LYAACaAEAAvnkbAAC55DqqoJOrCQE',
        'CAACAgIAAxkBAAEE3alikz13fkqt9-x4UdDTPaWRTW4y-QACrgEAAvnkbAABq56I9R5Ui8gkBA'
    ]
    bot.send_sticker(message.chat.id, random.choice(random_fail), reply_to_message_id=message.message_id)


# No
@bot.message_handler(regexp='нет|Нет|не хочу|Не хочу|неа|Неа')
def reply_no(message):
    random_no = [
        'CAACAgIAAxkBAAEE3l5ik29xNysfX9qCyfkQ1_QNLEB1FAACiQIAAvnkbAABen6D4HhGcz0kBA',
        'CAACAgIAAxkBAAEE3mBik290V034mwRRs1z0FwYhcd3YVAACgQIAAvnkbAABn8BL_mlx8eokBA',
        'CAACAgIAAxkBAAEE3mJik294Dymh6aJYqikyXDx6W56j4gACfwIAAvnkbAABLcA1yOHifyokBA',
        'CAACAgIAAxkBAAEE3lBik25QVR8bVcHWKrx4mQ9BGPlbFQACbQIAAvnkbAABefDvprRTIC8kBA',
        'CAACAgIAAxkBAAEE3lRik25X7cFMP29UTcMAAUcs44DzJdQAApkCAAL55GwAAT3hiwAB3ifFFCQE',
        'CAACAgIAAxkBAAEE3cFik0Ai_DIEeB1831yV7PeNj7HDoQAC2wEAAvnkbAABCX-hVktjtVAkBA',
        'CAACAgIAAxkBAAEE3bdikz8zDacAAQlJ0lZHK14dF2LigBcAAs4BAAL55GwAAep5oV8BxDHDJAQ',
        'CAACAgIAAxkBAAEE3bFikz4ErrqI0MidEbph4z3Lz88v2AACvwEAAvnkbAABHngR9XeKmpskBA',
        'CAACAgIAAxkBAAEEj_JiZ-SmicycnWRSK_7-BZ5j72STKAACFgADNIWFDIJkUm5I1EARJAQ',
        'CAACAgIAAxkBAAEEj_RiZ-Sy6miUcHcm6NL3OO7EB_3VuAACiAADNIWFDAABqwuTmC7SfyQE',
        'CAACAgIAAxkBAAEEj_ZiZ-TTFFzjrf-ueOznUc2Y__C2igACMwADNIWFDBq9FdX0dn0HJAQ',
        'CAACAgIAAxkBAAEEj_5iZ-Xv7zWLEubFh3G07MjI5DioRAACSgADTMV6AAEx8gcxzSQPoSQE',
        'CAACAgIAAxkBAAEEkAABYmfl-KWwkCgx7Xwa0lSkm3OI7QYAAkcAA0zFegAB1maqhl0buSEkBA',
        'CAACAgIAAxkBAAEEkEpiZ-f16B9vmRD0j0Si3VCNeXWN4QACbgADNIWFDHs7LxuxsQUKJAQ',
        'CAACAgIAAxkBAAEEkG9iZ-iB78NDnPUynJYOlBkyuiYTOQACLwADNIWFDB77Qd24HYDRJAQ',
        'CAACAgIAAxkBAAEEkI1iZ-lcS8oGFuVhDb9VCR-TfW8E2AACKQADa2iODohSkyEHad-9JAQ',
        'CAACAgIAAxkBAAEEk99iajmbasdRpugnTxgh7qawJ_gTogACGAAD5HgnCFl4jWsIs-n0JAQ',
        'CAACAgIAAxkBAAEElBFiajpPmCOg1WIL8sObZJ5DcvHRdAACPwAD5HgnCAgv8ObTQaVXJAQ',
        'CAACAgIAAxkBAAEElKpiam-obsF3g5b0ApLFGXs2NQfwJgACfQEAAvnkbAABO9ZcmonHiJYkBA',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_no), reply_to_message_id=message.message_id)


# When
@bot.message_handler(regexp='когда|Когда|когда?|Когда?|скоро|Скоро')
def reply_when(message):
    random_when = [
        'CAACAgIAAxkBAAEE3mhik3AjB23s6-Ojv6_UQK3WB2kipgACdQIAAvniAAB8erfWz9rKMQkBA',
        'CAACAgIAAxkBAAEE3btikz865KIe3VWAfMcZdeMtlkVBNgACzAEAAvnkbAABHBEfcOGSvIMkBA',
        'CAACAgIAAxkBAAEE3bNikz4HESySv1wFn5KwKDTEWrxD1wACvgEAAvnkbAABP6ZugGkwQxokBA',
        'CAACAgIAAxkBAAEEj-ZiZ-OldoHlNXJXWExBkZfgenaSHAACEAADNIWFDGaZ6_mOatb4JAQ',
        'CAACAgIAAxkBAAEEkDBiZ-cTmhgztwtUVit4WOiyVFCvaQAC-AcAAtjY4QABIxxiYVEVKLwkBA',
        'CAACAgIAAxkBAAEE3aFikz1r1U-G2SosrNge45oAAR3A_sIAArQBAAL55GwAASx_ZOFr8MyYJAQ',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_when), reply_to_message_id=message.message_id)


# Hello
@bot.message_handler(regexp='привет|Привет|здорова|Здорова|здрасьте|Здрасьте|здравствуйте|Здравствуйте|приветствую|'
                            'Приветствую|шалом|Шалом|бонжур|Бонжур|гутентак|Гутентак|хеллоу|Хеллоу|хай|Хай|здравствуй|'
                            'Здравствуй|здраствуйте|Здраствуйте|здрасвтуй|Здраствуй|здарова|Здарова')
def reply_hello(message):
    random_hello = [
        'CAACAgIAAxkBAAEE3Z9ikz0xn797sstjzyx_3o4PnzbxFgACpgEAAvnkbAABoXukcJk-kVEkBA',
        'CAACAgIAAxkBAAEE3YNikziFlCesE7X-7zV_eWw0wOAN0gAC9wEAAvnkbAAB8KywR8WwpQ8kBA',
        'CAACAgIAAxkBAAEE3X9ikzhKLZttH0u49GWtwP2sTG6jagAC1QEAAvnkbAABdj_TZWmpU5ckBA',
        'CAACAgIAAxkBAAEEk-Fiajmil9w2HSGAreyyAAHOMUuiOTkAAhkAA-R4JwgxQ_dJwjYxriQE',
        'CAACAgIAAxkBAAEEj91iZ-Im6qvyLM_QaSyEQas1uRYnGwACHQMAAu93BwABx7bJkbbUuWIkBA',
        'CAACAgIAAxkBAAEEj99iZ-N6zTV7Rwc0ZCsfxjWv2cCabwAC6wcAAtjY4QABdEVk37HA_PwkBA',
        'CAACAgIAAxkBAAEEk81iajlQ1hxNrbLU24_rqqdVJKT7ZQACCwAD5HgnCPlr1okCh0T6JAQ',
        'CAACAgIAAxkBAAEEkARiZ-YCcT_AYVS9wOm2XGkXkseFcgACTAADTMV6AAGeeLikLMRieiQE',
        'CAACAgIAAxkBAAEEkCRiZ-bg4SHeYNwsQKvKNnFYMzwuIwACrwcAAipVGAI94NWJRQJRgCQE',
        'CAACAgIAAxkBAAEEkEBiZ-ecIbYTqkZYXSdniYq8SAokrgACqQADNIWFDD538oyz8HFZJAQ',
        'CAACAgIAAxkBAAEEkERiZ-e-H2-ARmNY7gsaqK2V6nOznwACgQADNIWFDNDwkGMTBh8WJAQ',
        'CAACAgIAAxkBAAEEkEZiZ-e_fXv_o1TTW-Co0_cSPD8NagACfwADNIWFDCwPXWgNEUKeJAQ',
        'CAACAgIAAxkBAAEEkEhiZ-faRYHAAAEK9KEG1Go8-Kr58OQAAnUAAzSFhQxOPiZwDYs6tSQE',
        'CAACAgIAAxkBAAEEk9diajl_QNgRkuFCknsX25kYXrirewACFAAD5HgnCF43MRGpkoGoJAQ',
        'CAACAgIAAxkBAAEEk-9iajnogjZEvdzZqLyIBa3VXvLUkQACLQAD5HgnCI484VsjQzJmJAQ',
        'CAACAgIAAxkBAAEEk_1iajoUChQx2TvFNlg_yoVUHw7OkQACNgAD5HgnCNiv2IHlSkooJAQ',
        'CAACAgIAAxkBAAEElJJiam8GiuMu58zvdJExrWfSeZW4iQACPgEAAvnkbAABCxxGn_KfrDgkBA',
        'CAACAgIAAxkBAAEElJ5iam9D5h3rTow-vKcuSM6vDI_5uwACTAEAAvnkbAABNzS3k8LNs3UkBA',
        'CAACAgIAAxkBAAEElKhiam-gdYwUwRLUySZezzR6wbKMogACfAEAAvnkbAAB2L9RHCpOjW8kBA',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_hello), reply_to_message_id=message.message_id)


# Crash
@bot.message_handler(regexp='сломался|Сломался|Бот не работает|бот не работает|бот не отвечает|бот не отвечает|почини|'
                            'Почини|чиню|Чиню|починить|Починить|чинить|Чинить')
def reply_crash(message):
    random_crash = [
        'CAACAgIAAxkBAAEEkHtiZ-jymT1KTeTPKUOEoD-g-wyNmwAC1BEAA8CgSXknAeKPK_QMJAQ',
        'CAACAgIAAxkBAAEEkIViZ-ks1ALZV0FY2mrdUnRJuw7oyAACLQ8AAvNDKEhYkX4ZhSprPyQE',
    ]
    bot.send_sticker(message.chat.id, random.choice(random_crash), reply_to_message_id=message.message_id)


# Electrostatic
@bot.message_handler(regexp='статик|Статик|электростатик|Электростатик')
def reply_electrostatic(message):
    bot.send_message(message.chat.id, 'Все мои миксы можешь послушать тут: https://soundcloud.com/djelectrostatic')


# Rustam
@bot.message_handler(regexp='рустам|Рустам|рустаму|Рустаму|рустама|Рустама')
def reply_rustam(message):
    bot.send_message(message.chat.id, 'Рустам мой друг!')


# Artem
@bot.message_handler(regexp='артём|Артём|артему|Артёму|артёма|Артёма|артем|Артем')
def reply_artem(message):
    bot.send_message(message.chat.id, 'Артём мой друг!')


# Vanya
@bot.message_handler(regexp='ваня|Ваня|ване|Ване|вань|Вань|иван|Иван|вани|Вани')
def reply_vanya(message):
    bot.send_message(message.chat.id, 'Ваня мой друг!')


# Vlad
@bot.message_handler(regexp='влад|Влад|владу|Владу|влада|Влада')
def reply_vlad(message):
    bot.send_message(message.chat.id, 'Влад мой друг!')


# Kolya
@bot.message_handler(regexp='коля|Коля|коле|Коле|коль|Коль|николай|Николай|коли|Коли')
def reply_kolya(message):
    bot.send_message(message.chat.id, 'Коля мой друг!')


# Leha
@bot.message_handler(regexp='лёха|Лёха|лёхе|Лёхе|лёх|Лёх|алексей|Алексей|лёху|Лёху|лёхи|Лёхи')
def reply_leha(message):
    bot.send_message(message.chat.id, 'Лёха мой друг!')


# Azat
@bot.message_handler(regexp='азат|Азат|азату|Азат|азата|Азата|азатом|Азатом')
def reply_azat(message):
    bot.send_message(message.chat.id, 'Азат мой друг!')


# Denis
@bot.message_handler(regexp='денис|Денис|денису|Денису|дениса|Дениса|денисом|Денисом')
def reply_denis(message):
    bot.send_message(message.chat.id, 'Денис лучший друг Артёма!')


# Victor
@bot.message_handler(regexp='виктор|Виктор|вите|Вите|вити|Вити|витя|Витя|витей|Витей')
def reply_victor(message):
    bot.send_message(message.chat.id, 'Витя наш друг!')


# Dubs
@bot.message_handler(regexp='дабс|Дабс|дабсу|Дабсу|дабса|Дабса|дабсом|Дабсом|максдабс|Максдабс')
def reply_dubs(message):
    bot.send_message(message.chat.id, 'Макс мой друг!')


# Igor
@bot.message_handler(regexp='игорь|Игорь|игорю|Игорю|игоря|Игоря|large|Large|ларч|Ларч')
def reply_dubs(message):
    bot.send_message(message.chat.id, 'Игорь мой друг!')


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200


if __name__ == '__main__':
    start_process()
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

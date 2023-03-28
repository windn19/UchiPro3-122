import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from settings_new import telegram_token, api_token, EMOJI_CODE

TOKEN = telegram_token
API_KEY = api_token
URL_WEATHER_API = 'https://api.openweathermap.org/data/2.5/weather'

bot = telebot.TeleBot(TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Получить погоду', request_location=True))
keyboard.add(KeyboardButton('О проекте'))


def get_weather(lat='', lon='', loc=None):
    params = {'lat': lat,
              'lon': lon,
              'lang': 'ru',
              'units': 'metric',
              'appid': API_KEY} if not loc else {'q': loc,
                                                 'lang': 'ru',
                                                 'units': 'metric',
                                                 'appid': API_KEY}
    response = requests.get(url=URL_WEATHER_API, params=params)
    if response.status_code != 200:
        return 'Неизвестное название населенного пункта,\n попробуйте геолокацию'
    else:
        response = response.json()
        city_name = response['name']
        description = response['weather'][0]['description']
        code = response['weather'][0]['id']
        temp = response['main']['temp']
        temp_feels_like = response['main']['feels_like']
        humidity = response['main']['humidity']
        emoji = EMOJI_CODE[code]
        message = f'🏙 Погода в: {city_name}\n'
        message += f'{emoji} {description.capitalize()}.\n'
        message += f'🌡 Температура {temp}°C.\n'
        message += f'🌡 Ощущается {temp_feels_like}°C.\n'
        message += f'💧 Влажность {humidity}%.\n'
        return message


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # pprint(message.json)
    text = 'Отправь мне свое местоположение и я отправлю тебе погоду.'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.message_handler(regexp='О проекте')
def send_about(message):
    text = 'Бот позволяет получить погоду в текущем местоположении!\n'
    text += 'Для получения погоды - отправь боту геопозицию.\n'
    text += 'Погода берется с сайта https://openweathermap.org.\n'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_city(message):
    result = get_weather(loc=message.text.strip())
    bot.send_message(message.chat.id, result, reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def send_weather(message):
    lon = message.location.longitude
    lat = message.location.latitude
    result = get_weather(lat, lon)
    bot.send_message(message.chat.id, result, reply_markup=keyboard)


bot.infinity_polling()
# https://github.com/batir8888/telegram_chat_bot.git

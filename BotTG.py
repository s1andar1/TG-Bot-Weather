import json
import telebot
import requests

bot = telebot.TeleBot('6822893818:AAF5ZLSQhX2P2N9hz0M4EItEmCwYax04tfI')
API = '91e596fd0a02743bc59982341a110f09'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}!\nРад тебя видеть!\nНапиши название города!')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')

    if res.status_code == 200:
        data = json.loads(res.text)
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        wind = data['wind']['speed']
        visibility = data['visibility']

        bot.reply_to(message,
                     f'{city.title()}, погода на данный момент:'
                     f'\n'
                     f'\nТемпература: {temp} °C'
                     f'\nСкорость ветра: {wind} м/с'
                     f'\nВидимость: {visibility / 1000} км')

        image = requests.get(f'http://openweathermap.org/img/wn/{icon}.png')
        with open('icon.png', 'wb') as f:
            f.write(image.content)
        image_weather = 'icon.png'
        file = open(image_weather, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, f'Город указан не верно')


bot.infinity_polling()

import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatActions
from aiogram.utils import executor

TOKEN = os.getenv('6001506268:AAFDK0Jk0tcMN7CjgoRJZdFGZruQV29obBM')
bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот погоды. Введите название города, чтобы узнать погоду.")


@dp.message_handler()
async def get_weather(message: types.Message):
    city = message.text
    try:
        api_key = os.getenv('API_KEY')
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ru&units=metric'
        response = requests.get(url).json()
        weather = response['weather'][0]['description']
        temp = response['main']['temp']
        feels_like = response['main']['feels_like']

        await bot.send_message(message.chat.id,
                               f"Погода в городе {city}: {weather}. Температура: {temp} °C (ощущается как {feels_like} °C).")
    except:
        await bot.send_message(message.chat.id,
                               "Не удалось получить погоду. Проверьте правильность ввода названия города.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
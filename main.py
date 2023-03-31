from random import randint
import asyncio
import os

import psycopg2

from googletrans import Translator

import pymorphy2

from datetime import datetime

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

from config import TOKEN

import requests
from bs4 import BeautifulSoup

bot_loop = asyncio.new_event_loop()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


import pandas as pd

@dp.message_handler(content_types=["document"])
async def file_manage(message: types.Message):
    user_id = 0
    user_id = message.from_user.id
    await message.document.download(destination="C:/Users/grish/OneDrive/Рабочий стол/проекты/PyCharm/бот Henry/file/table.xlsx")


if __name__ == '__main__':
    myloop = asyncio.new_event_loop()
    myloop.create_task(dp.start_polling())
    myloop.run_forever()
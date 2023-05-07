from random import randint
import asyncio
import os

import psycopg2

from googletrans import Translator

import pymorphy2

from datetime import datetime

import fake_useragent

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

from config import TOKEN

import requests
from bs4 import BeautifulSoup
bot_loop = asyncio.new_event_loop()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
name_file =""

import pandas as pd

import numpy as np


@dp.callback_query_handler(text=['pars_chek'])
async def process_start_command(message: types.Message):
    answer = steel_phoenix_pars(0)
    # await bot.send_message(message.from_user.id,f'{answer}')
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="audit_processing", callback_data="audit_processing"))
    keyboard.add(types.InlineKeyboardButton(text="pars_chek", callback_data="pars_chek"))
    keyboard.add(types.InlineKeyboardButton(text="match_count", callback_data="match_count"))
    await message.answer("Вас приветсвует личный помошник Henry чем я могу помочь вам",reply_markup=keyboard)
@dp.message_handler(commands=['function_menu'])
async def process_start_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="audit_processing", callback_data="audit_processing"))
    keyboard.add(types.InlineKeyboardButton(text="pars_chek", callback_data="pars_chek"))
    keyboard.add(types.InlineKeyboardButton(text="match_count", callback_data="match_count"))
    await message.answer("Вас приветсвует личный помошник Henry выберете оду из ниже предложенных функций",reply_markup=keyboard)


@dp.callback_query_handler(text="match_count")
async def processing_message(message: types.Message):
    await bot.send_message(message.from_user.id, "Пожалуйста укажите название под которым вы хотите сохранить этот файл")
    @dp.message_handler()
    async def processing_message(message: types.Message):
        global name_file
        name_file = message.text
        await bot.send_message(message.from_user.id,"теперь отправте мене ваш файл в фармате .xlsx")
        save_file("match")





@dp.callback_query_handler(text="audit_processing")
async def processing_message(message: types.Message):
    await bot.send_message(message.from_user.id,"Пожалуйста укажите название под которым вы хотите сохранить этот файл")
    @dp.message_handler()
    async def processing_message(message: types.Message):
        global name_file
        name_file = message.text
        await bot.send_message(message.from_user.id, "теперь отправте мене ваш файл в фармате .xlsx")
        save_file("audit")


def save_file (key):
    @dp.message_handler(content_types=["document"])
    async def file_manage(message: types.Message):
        global name_file
        await message.document.download(destination=f'file\{key}\{name_file}.xlsx')
        await bot.send_message(message.from_user.id, "Отлично ваш файл был успешно сахранён, начинаю оработку это может занять некоторое время ")
        if (key == "match"):
            count_mach(name_file ,message.from_user.id )
            await bot.send_message(message.from_user.id,"обработка файла завершена отправляю вам финальну сводку \n /function_menu")
            f = open(f'file\\match\\{name_file}_result.xlsx',"rb")
            await bot.send_document(message.chat.id, f)
        elif(key == "audit"):
            count_mach(name_file,message.from_user.id)
            await bot.send_message(message.from_user.id,"обработка файла завершена отправляю вам финальный результат \n /function_menu")
            f = open(f'file\\audit\\{name_file}_result.xlsx', "rb")
            await bot.send_document(message.chat.id, f)



def steel_phoenix_pars(audit , id):
    file = pd.read_excel(f'file\\audit\\{name_file}.xlsx')
    file.head()

    url = 'https://steel-phoenix.ru/sc/report/auditcheck.php'
    login = 'IvanFlay3r'
    password = 'U4pcWqH4n'

    session = requests.Session()
    session.auth = (login, password)

    response = session.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Найдите поле с ссылкой и вставьте передаваемый текст
    link_field = soup.find('input', {'name': 'link'})
    link_field['value'] = 'https://example.com'

    # Отправьте форму
    response = session.post(url, data=soup.select_one('form').attrs['data-ajax-form'])
    print(response.text)
    return response

def count_mach(name_file , id ):
    # cols_user_base = [1, 3, 4, 9, 11]
    file = pd.read_excel(f'file\\match\\{name_file}.xlsx')
    file.head()
    result = pd.DataFrame({ 'Date/name': []})
    df = pd.DataFrame(result, columns=[ 'Date/name'])
    result = pd.concat([result, df], ignore_index=True, sort=False)
    result.to_excel(f'file\\match\\{name_file}_result.xlsx')
    result = pd.read_excel(f'file\\match\\{name_file}_result.xlsx')
    result.head()
    name = file['Alias'].tolist()
    Start_Date = (file['Period'].tolist())
    Speed = file['Speed'].tolist()
    Games = file['Games'].tolist()
    lengh = name.index(False)
    percent = lengh / 100
    for nuber in range(0, lengh):
        print(f'{nuber / percent} %')
        print(nuber)
        if str(name[nuber]) ==('Freedoom'):
            print("fak")
        Name_result = (result.columns.ravel())
        Date = result['Date/name'].tolist()

        # if Speed[nuber] == 'Flash' or Speed[nuber] == 'GG' or Speed[nuber] == 'Nitro':
        #     count = 3 * Games[nuber]
        # elif Speed[nuber] == 'Winamax' or Speed[nuber] == 'WMX':
        #     count = 3 * Games[nuber]
        # elif Speed[nuber] == 'Normal':
        #     count = 1 * Games[nuber]

        if (str(name[nuber]) in str(Name_result)) == False:
            if ((str(Start_Date[nuber])[0:7]) in Date):
                boolean_variable = -1
                while boolean_variable == -1:
                    index = 0
                    for index in range(len(Date)):
                        if (str(Start_Date[nuber])[0:7]) == (Date[index]):
                            boolean_variable = index
                    if boolean_variable != -1:
                        if Speed[nuber] == 'Flash' or Speed[nuber] == 'GG' or Speed[nuber] == 'Nitro':
                            count = 3 * Games[nuber]
                        elif Speed[nuber] == 'Winamax' or Speed[nuber] == 'WMX':
                            count = 3 * Games[nuber]
                        elif Speed[nuber] == 'Normal':
                            count = 1 * Games[nuber]
                        isNan = True
                        df = pd.DataFrame( columns=['Date/name', f'{[name[nuber]]}'])
                        result = pd.concat([result, df], ignore_index=True, sort=False)
                        if isNan == np.isnan(result.at[boolean_variable, f'{[name[nuber]]}']): #Хрень
                            result.at[boolean_variable, f'{[name[nuber]]}'] = count
                        else:
                            result.at[boolean_variable, f'{[name[nuber]]}'] += count

                        result.to_excel(f'file\\match\\{name_file}_result.xlsx')
                    else:
                        boolean_variable = 0
                        if Speed[nuber] == 'Flash' or Speed[nuber] == 'GG':
                            count = 3 * Games[nuber]
                        elif Speed[nuber] == 'Winamax' or Speed[nuber] == 'WMX':
                            count = 3 * Games[nuber]
                        elif Speed[nuber] == 'Normal':
                            count = 1 * Games[nuber]
                        elif Speed[nuber] == 'Nitro':
                            count = Games[nuber] / 3
                        new_player = ({ 'Date': [(str(Start_Date[nuber])[0:7])],f'{[name[nuber]]}':[count] })
                        df = pd.DataFrame(new_player, columns=[ 'Date/name' , f'{[name[nuber]]}'])
                        result = pd.concat([result, df], ignore_index=True, sort=False)
                        result.to_excel(f'file\\match\\{name_file}_result.xlsx')

            else:
                if Speed[nuber] == 'Flash' or Speed[nuber] == 'GG':
                    count = 3 * Games[nuber]
                elif Speed[nuber] == 'Winamax' or Speed[nuber] == 'WMX':
                    count = 3 * Games[nuber]
                elif Speed[nuber] == 'Normal':
                    count = 1 * Games[nuber]
                elif Speed[nuber] == 'Nitro':
                    count = Games[nuber] / 3
                new_player = ({'Date/name': [(str(Start_Date[nuber])[0:7])] , f'{[name[nuber]]}':[count]})
                df = pd.DataFrame(new_player, columns=['Date/name', f'{[name[nuber]]}'])
                result = pd.concat([result, df], ignore_index=True, sort=False)
                result.to_excel(f'file\\match\\{name_file}_result.xlsx')
        elif ((str(Start_Date[nuber])[0:7]) in Date):
            boolean_variable = -1
            while boolean_variable == -1:
                index = 0
                for index in range(len(Date)):
                    if (str(Start_Date[nuber])[0:7]) == (Date[index]):
                        boolean_variable = index
                if boolean_variable != -1:
                    if Speed[nuber] == 'Flash' or Speed[nuber] == 'GG' or Speed[nuber] == 'Nitro':
                        count = 3 * Games[nuber]
                    elif Speed[nuber] == 'Winamax' or Speed[nuber] == 'WMX':
                        count = 3 * Games[nuber]
                    elif Speed[nuber] == 'Normal':
                        count = 1 * Games[nuber]

                    df = pd.DataFrame(columns=[ f'{[name[nuber]]}'])
                    result = pd.concat([result, df], ignore_index=True, sort=False)
                    isNan = True
                    if isNan == np.isnan(result.at[boolean_variable, f'{[name[nuber]]}']):  # Хрень
                        result.at[boolean_variable, f'{[name[nuber]]}'] = count
                    else:
                        result.at[boolean_variable, f'{[name[nuber]]}'] += count
                    result.to_excel(f'file\\match\\{name_file}_result.xlsx')
                else:
                    boolean_variable = 0
                    if Speed[nuber] == 'Flash' or Speed[nuber] == 'GG':
                        count = 3 * Games[nuber]
                    elif Speed[nuber] == 'Winamax' or Speed[nuber] == 'WMX':
                        count = 3 * Games[nuber]
                    elif Speed[nuber] == 'Normal':
                        count = 1 * Games[nuber]
                    elif Speed[nuber] == 'Nitro':
                        count = Games[nuber] / 3
                    new_player = ({f'{[name[nuber]]}':[count]})
                    df = pd.DataFrame(new_player, columns=[ f'{[name[nuber]]}'])
                    result = pd.concat([result, df], ignore_index=True, sort=False)
                    result.to_excel(f'file\\match\\{name_file}_result.xlsx')
        else:
            if Speed[nuber] == 'Flash' or Speed[nuber] == 'GG':
                count = 3 * Games[nuber]
            elif Speed[nuber] == 'Winamax' or Speed[nuber] == 'WMX':
                count = 3 * Games[nuber]
            elif Speed[nuber] == 'Normal':
                count = 1 * Games[nuber]
            elif Speed[nuber] == 'Nitro':
                count = Games[nuber] / 3
            new_player = ({'Date/name': [(str(Start_Date[nuber])[0:7])], f'{[name[nuber]]}':[count]})
            df = pd.DataFrame(new_player, columns=['Date/name', f'{[name[nuber]]}'])
            result = pd.concat([result, df], ignore_index=True, sort=False)
            result.to_excel(f'file\\match\\{name_file}_result.xlsx')


if __name__ == '__main__':
    myloop = asyncio.new_event_loop()
    myloop.create_task(dp.start_polling())
    myloop.run_forever()
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
            f = open(f'file\match\{name_file}_result.xlsx',"rb")
            await bot.send_document(message.chat.id, f)





def steel_phoenix_pars(audit):
    link = 'https://steel-phoenix.ru/sc/report/auditcheck.php'
    session =requests.Session()
    user = fake_useragent.UserAgent().random
    log_data ={
        "username": "IvanFlay3r",
        "password": "U4pcWqH4n",
        "g - recaptcha - response": "03",
        # AKH6MRFybb - cQuItAjK0kAHxVN1js7pJnirZ_8j9ykNwFzRg3sZcWWyLwv9JAL8Cgi2FzO1o_i2thuvygSTDuXWILgWfv3uihkuKe9DPTVnprQQYyVABK_d2 - y5NtKYLll_Vl_bG4BA1_x - zh8Sz0abUtKRgueEsJHZuqDT9r0roBB5hhpES7_ugO6MUzPXEw4KaVrItgnlk7096zr7XEeZuynxvTdVPVN4pLTsfu98j_JRSWv - Ugrd - UGkmxPM8FTKsr6cUlkWETOC0m6JReo5s1PGB6S0OPtMZw4d_0ug7GSbKZZG4NB7J8xlic0_o_eh4_p6pJrFEiV - -y5smWMo_KaSnunUxdGGUUF4rBiTw5kIAv7AGigCEWz23MuJzOUi4oret5QbqkCBQbIuqAfQMBzzKXGA8aKgsxfTwNgyZ - m9oZWqzb66_0jdZxTJsxmKsRDWX4RzJMF7MC - bij3FEij9UAoUbrZcNFcWnrlpSYQh - SYTuwIDZVF_wfOAuQsNeKXSWhD - S
            "lang": "en",
    "g - recaptcha - response": "03",
    # AKH6MRFybb - cQuItAjK0kAHxVN1js7pJnirZ_8j9ykNwFzRg3sZcWWyLwv9JAL8Cgi2FzO1o_i2thuvygSTDuXWILgWfv3uihkuKe9DPTVnprQQYyVABK_d2 - y5NtKYLll_Vl_bG4BA1_x - zh8Sz0abUtKRgueEsJHZuqDT9r0roBB5hhpES7_ugO6MUzPXEw4KaVrItgnlk7096zr7XEeZuynxvTdVPVN4pLTsfu98j_JRSWv - Ugrd - UGkmxPM8FTKsr6cUlkWETOC0m6JReo5s1PGB6S0OPtMZw4d_0ug7GSbKZZG4NB7J8xlic0_o_eh4_p6pJrFEiV - -y5smWMo_KaSnunUxdGGUUF4rBiTw5kIAv7AGigCEWz23MuJzOUi4oret5QbqkCBQbIuqAfQMBzzKXGA8aKgsxfTwNgyZ - m9oZWqzb66_0jdZxTJsxmKsRDWX4RzJMF7MC - bij3FEij9UAoUbrZcNFcWnrlpSYQh - SYTuwIDZVF_wfOAuQsNeKXSWhD - S
    }
    header = {
        'user-agent': user
    }
    respose = session.post(link,data=log_data,headers= header ).text
    return respose

def count_mach(name_file , id ):
    # cols_user_base = [1, 3, 4, 9, 11]
    file = pd.read_excel(f'file\\match\\{name_file}.xlsx')
    file.head()
    result = pd.DataFrame({'Name': [], 'Games': [], 'Date': []})
    df = pd.DataFrame(result, columns=['Name', 'Games', 'Date'])
    result = pd.concat([result, df], ignore_index=True, sort=False)
    result.to_excel(f'file\match\{name_file}_result.xlsx')
    result = pd.read_excel(f'file\match\{name_file}_result.xlsx')
    result.head()
    name = file['Alias'].tolist()
    Start_Date = file['Period'].tolist()
    Speed = file['Speed'].tolist()
    Games = file['Games'].tolist()
    lengh = len(name)
    percent = lengh / 100
    progres = 0
    count_progres = 0
    for nuber in range(0, lengh):
        # if (nuber/percent - progres) >= 5:
        #     count_progres += 1
        #     bot.send_message(id,f'прогресс выполнения-{count_progres * 5}%')
        #     progres = nuber / percent
        # else:
        #     progres = nuber / percent
        print(f'{nuber / percent} %')
        Name_result = result['Name'].tolist()
        Games_result = result['Games'].tolist()
        Date = result['Date'].tolist()
        if (name[nuber] in Name_result) == False:
            if Speed[nuber] == 'Flash' or Speed[nuber] == 'GG':
                count =  3 * Games[nuber]
            elif Speed[nuber] == 'Winamax' or Speed[nuber] == 'WMX' :
                count = 3 * Games[nuber]
            elif Speed[nuber] == 'Normal':
                count = 1 * Games[nuber]
            elif Speed[nuber] == 'Nitro':
                count =  Games[nuber] / 3
            new_player = ({'Name': [name[nuber]], 'Games':[count], 'Date':[Start_Date[nuber]]})
            df = pd.DataFrame(new_player, columns=['Name','Games','Date'])
            result = pd.concat([result, df], ignore_index=True, sort=False)
            result.to_excel(f'file\match\{name_file}_result.xlsx')
        elif (Start_Date[nuber] in Date):
            boolean_variable = -1
            while boolean_variable == -1:
                index = 1
                for index in range(len(Name_result)):
                    if Name_result[index] == name[nuber] and Start_Date[nuber] == Date[index]:
                        boolean_variable = index
                if boolean_variable != -1:
                    if Speed[nuber] == 'Flash' or Speed[nuber] == 'GG':
                        count = 3 * Games[nuber]
                    elif Speed[nuber] == 'Winamax' or Speed[nuber] == 'WMX':
                        count = 3 * Games[nuber]
                    elif Speed[nuber] == 'Normal':
                        count = 1 * Games[nuber]
                    elif Speed[nuber] == 'Nitro':
                        count = Games[nuber] / 3
                    result.at[boolean_variable, 'Games'] = count + Games_result[boolean_variable]
                    result.to_excel(f'file\match\{name_file}_result.xlsx')
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
                    new_player = ({'Name': [name[nuber]], 'Games': [count], 'Date': [Start_Date[nuber]]})
                    df = pd.DataFrame(new_player, columns=['Name', 'Games', 'Date'])
                    result = pd.concat([result, df], ignore_index=True, sort=False)
                    result.to_excel(f'file\match\{name_file}_result.xlsx')
        else:
            if Speed[nuber] == 'Flash' or Speed[nuber] == 'GG':
                        count = 3 * Games[nuber]
            elif Speed[nuber] == 'Winamax' or Speed[nuber] == 'WMX':
                        count = 3 * Games[nuber]
            elif Speed[nuber] == 'Normal':
                        count = 1 * Games[nuber]
            elif Speed[nuber] == 'Nitro':
                count = Games[nuber] / 3
            new_player = ({'Name': [name[nuber]], 'Games': [count], 'Date': [Start_Date[nuber]]})
            df = pd.DataFrame(new_player, columns=['Name', 'Games', 'Date'])
            result = pd.concat([result, df], ignore_index=True, sort=False)
            result.to_excel(f'file\match\{name_file}_result.xlsx')


if __name__ == '__main__':
    myloop = asyncio.new_event_loop()
    myloop.create_task(dp.start_polling())
    myloop.run_forever()
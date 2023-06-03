import webbrowser
from random import randint
import asyncio
import os
import random
import psycopg2

from googletrans import Translator

import pymorphy2

from datetime import datetime

from fake_useragent import UserAgent

import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from config import TOKEN
import pytesseract
from PIL import Image
import requests
from bs4 import BeautifulSoup
bot_loop = asyncio.new_event_loop()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
name_file =""
global key

import pandas as pd

import numpy as np


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="audit_processing", callback_data="audit_processing"))
    keyboard.add(types.InlineKeyboardButton(text="match_count", callback_data="match_count"))
    await message.answer("Вас приветсвует личный помошник Henry чем я могу помочь вам",reply_markup=keyboard)
@dp.message_handler(commands=['function_menu'])
async def process_start_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="audit_processing", callback_data="audit_processing"))
    keyboard.add(types.InlineKeyboardButton(text="match_count", callback_data="match_count"))
    await message.answer("Вас приветсвует личный помошник Henry выберете оду из ниже предложенных функций",reply_markup=keyboard)


@dp.callback_query_handler(text="match_count")
async def processing_message(message: types.Message):
    await bot.send_message(message.from_user.id, "Пожалуйста укажите название под которым вы хотите сохранить этот файл")
    global key
    key = 'match'
    return key

@dp.message_handler()
async def processing_message(message: types.Message):
    global name_file , key
    if key != '':
        name_file = message.text
        await bot.send_message(message.from_user.id,"теперь отправте мене ваш файл в фармате .xlsx")
        save_file(key)
    else:
        await bot.send_message(message.from_user.id,"простите но я пока не умею отвечеть на такие запросы")





@dp.callback_query_handler(text="audit_processing")
async def processing_message(message: types.Message):
    await bot.send_message(message.from_user.id,"Пожалуйста укажите название под которым вы хотите сохранить этот файл")
    global key
    key = 'audit'
    return key

def save_file (key):
    @dp.message_handler(content_types=["document"])
    async def file_manage(message: types.Message):
        global name_file , key
        await message.document.download(destination=f'file\\{key}\\{name_file}.xlsx')
        await bot.send_message(message.from_user.id, "Отлично ваш файл был успешно сахранён, начинаю оработку это может занять некоторое время ")
        if (key == "match"):
            key = ''
            count_mach(name_file ,message.from_user.id )
            await bot.send_message(message.from_user.id,"обработка файла завершена отправляю вам финальну сводку \n /function_menu")
            f = open(f'file\\match\\{name_file}_result.xlsx',"rb")
            await bot.send_document(message.chat.id, f)
            return key
        elif(key == "audit"):
            key = ''
            steel_phoenix_pars(name_file,message.from_user.id)
            await bot.send_message(message.from_user.id,"обработка файла завершена отправляю вам финальный результат \n /function_menu")
            f = open(f'file\\audit\\{name_file}_result.xlsx', "rb")
            await bot.send_document(message.chat.id, f)
            return key




def steel_phoenix_pars(audit , id):

    url = 'https://steel-phoenix.ru'
    login = 'IvanFlay3r'
    password = 'U4pcWqH4n'

    driver = webdriver.Chrome()
    driver.get(url)

    login_button = driver.find_element(By.ID,"login-switch")
    login_button.click()

    # Находим поля для ввода логина и пароля
    username_field = driver.find_element(By.NAME,'username')
    password_field = driver.find_element(By.NAME,'password')

    # Вводим логин и пароль
    username_field.send_keys(login)
    password_field.send_keys(password)

    # Нажимаем кнопку "Войти"
    login_button = driver.find_element(By.ID,"send-form-button")
    login_button.click()

    time.sleep(1)
    main_window = driver.current_window_handle
    audit_chek = driver.find_element(By.XPATH,"//*[text()='Audit check']" )
    audit_chek.click()

    print("Fuk this captcha")

    file = pd.read_excel(f'file\\audit\\{audit}.xlsx')
    file.head()
    periud_list = (file['Timestamp'].tolist())
    Name_list = (file['Никнейм на Pokerstars.com'].tolist())
    link_list = file['Ссылка на аудит Pokerstars.com'].tolist()
    lengh = len(Name_list)
    result_file = pd.DataFrame({'Alias': [], 'Timestamp': [], 'Speed': [],'StakeName': [], 'Stake': [], 'Games': [],'Profit':[], 'RB': []})
    df = pd.DataFrame(result_file, columns=['Alias', 'Timestamp', 'Speed', 'StakeName', 'Stake', 'Games','Profit', 'RB'])
    result_file = pd.concat([result_file, df], ignore_index=True, sort=False)
    result_file.to_excel(f'file\\audit\\{name_file}_result.xlsx')
    result_file = pd.read_excel(f'file\\audit\\{name_file}_result.xlsx')
    result_file.head()
    driver.switch_to.window(driver.window_handles[-1])
    for number in range(80, lengh): #заменить на 0 в финалке или придумать отсцёт
        print(number)
        response = requests.get(link_list[number])
        if ("404 Not Found" in str(response.content)) == False:
            print("start")
            link = driver.find_element(By.ID,"urla")
            driver.find_element(By.ID, "urla").clear()
            link.send_keys(link_list[number])

            chek = driver.find_element(By.ID, "startbut")
            chek.click()
            time.sleep(1)
            result = driver.find_element(By.CLASS_NAME, "container")
            result = result.get_attribute('outerHTML')
            s_1 = result.find("Results:")
            s_2 = result.find("Deal:")
            result = result[s_1:s_2]
            if ("Jack:" in result):
                if ("Lost;" in result):
                    dictionary = {f'{result[result.find("Jack:"):(result.find("Lost;")+5)]}':""}
                    result = multiple_replace(result, dictionary)
                elif ("Won;" in result):
                    dictionary = {f'{result[result.find("Jack:"):(result.find("Won;") + 4)]}': ""}
                    result = multiple_replace(result, dictionary)
            dictionary = {"</b>": "","<br>":"","<div>":"","<b>":"",f'<div class="audit_block_wrap"> ':""}
            result = multiple_replace(result, dictionary)
            if ("No data" in result):
                new_entry = ({'Alias': [Name_list[number]], 'Timestamp': [(str(periud_list[number]))[0:10]]
                    , 'RB': [result[result.find('RB: 		Total: ') + 13:result.find('$		Chest:')]]})
                df = pd.DataFrame(new_entry, columns=['Alias', 'Timestamp', 'Speed', 'StakeName', 'Stake', 'Games','Profit', 'RB'])
                result_file = pd.concat([result_file, df], ignore_index=True, sort=False)
                result_file.to_excel(f'file\\audit\\{name_file}_result.xlsx')
            count = result.count('Profit')
            for number_2 in range(0,count):
                print( f'{result}_befor')
                # print(result[result.find('$')+1:result.find('-')])
                if (result[result.find('$')+1:result.find('-')]) == ' ':
                    if number_2 != count - 1:
                        first_index = result.find('$')
                        second_index = result.find('$', first_index + 1)
                        last_RB_spase = 0
                        if 'Results:  ' in result:
                            last_RB_spase = 10
                        elif 'Results: ' in result:
                            last_RB_spase = 9
                        new_entry = ({'Alias':[Name_list[number]] ,'Timestamp':[(str(periud_list[number]))[0:10]]
                            ,'Speed':['Normal']
                            ,'StakeName': ['$' + result[result.find('Results:') + 9:result.find('$')]]
                            ,'Stake':[result[result.find('Results:')+last_RB_spase:result.find('$')]]
                            ,'Games':[result[result.find('$ - ')+4:result.find(' spins')]]
                            ,'Profit':[result[result.find('Profit: ')+8:second_index]]})
                        df = pd.DataFrame(new_entry, columns=['Alias', 'Timestamp', 'Speed', 'StakeName', 'Stake', 'Games','Profit', 'RB'])
                        result_file = pd.concat([result_file, df], ignore_index=True, sort=False)
                        result_file.to_excel(f'file\\audit\\{name_file}_result.xlsx')
                        result = result[:result.find('Results:') ] + result[second_index + 2:]
                        result ='Results: '+ result
                        print( f'{result}_after')
                    else:
                        first_index = result.find('$')
                        second_index = result.find('$', first_index + 1)
                        last_RB_spase = 0
                        if 'Results:  ' in result:
                            last_RB_spase = 10
                        elif 'Results: ' in result:
                            last_RB_spase = 9
                        new_entry = ({'Alias': [Name_list[number]], 'Timestamp': [(str(periud_list[number]))[0:10]]
                            , 'Speed': ['Normal']
                            , 'StakeName': ['$' + result[result.find('Results:') + 9:result.find('$')]]
                            , 'Stake': [result[result.find('Results:') + last_RB_spase:result.find('$')]]
                            , 'Games': [result[result.find('$ - ') + 4:result.find(' spins')]]
                            , 'Profit': [result[result.find('Profit: ')+8:second_index]]
                            , 'RB': [result[result.find('RB: 		Total: ') + 13:result.find('$		Chest:')]]})
                        df = pd.DataFrame(new_entry, columns=['Alias', 'Timestamp', 'Speed', 'StakeName', 'Stake', 'Games','Profit', 'RB'])
                        result_file = pd.concat([result_file, df], ignore_index=True, sort=False)
                        result_file.to_excel(f'file\\audit\\{name_file}_result.xlsx')
                        result = result[:result.find('Results:')] + result[second_index + 2:]
                        result = 'Results: ' + result
                        print(f'{result}_after')
                else:
                    if number_2 != count - 1:
                        if "(1million)" in result[result.find('$ ')+1:result.find(' - ')]:
                            first_index = result.find('$')
                            second_index = result.find('$', first_index + 1)
                            last_RB_spase = 0
                            if 'Results:  ' in result:
                                last_RB_spase = 10
                            elif 'Results: ' in result:
                                last_RB_spase = 9
                            if '' in result[result.find('(1million) ') + 10:result.find(' - ')]:
                                new_entry = (
                                {'Alias': [Name_list[number]], 'Timestamp': [(str(periud_list[number]))[0:10]]
                                    , 'Speed': ['Normal']
                                    , 'StakeName': ['$' + result[result.find('Results:') + last_RB_spase:result.find('$')]  + ' (1M)']
                                    , 'Stake': [(result[result.find('Results:') + 9:result.find('$')])]
                                    , 'Games': [result[result.find(' - ') + 3:result.find(' spins')]]
                                    , 'Profit': [result[result.find('Profit: ') + 8:second_index]]})
                            else:
                                new_entry = ({'Alias': [Name_list[number]], 'Timestamp': [(str(periud_list[number]))[0:10]]
                                    , 'Speed': [result[result.find('(1million) ') + 10:result.find(' - ')]]
                                    , 'StakeName': ['$' + result[result.find('Results:') + last_RB_spase:result.find('$')] + ' (1M) ' + result[result.find('$ ')+2:result.find(' - ')]]
                                    , 'Stake': [(result[result.find('Results:') + 9:result.find('$')])]
                                    , 'Games': [result[result.find(' - ') + 3:result.find(' spins')]]
                                    , 'Profit': [result[result.find('Profit: ')+8:second_index]]})
                            df = pd.DataFrame(new_entry,
                                              columns=['Alias', 'Timestamp', 'Speed', 'StakeName', 'Stake', 'Games','Profit', 'RB'])
                            result_file = pd.concat([result_file, df], ignore_index=True, sort=False)
                            result_file.to_excel(f'file\\audit\\{name_file}_result.xlsx')
                            result = result[:result.find('Results:')] + result[second_index + 2:]
                            result = 'Results: ' + result
                            print(f'{result}_after')
                        else:
                            first_index = result.find('$')
                            second_index = result.find('$', first_index + 1)
                            last_RB_spase = 0
                            if 'Results:  ' in result:
                                last_RB_spase = 10
                            elif 'Results: ' in result:
                                last_RB_spase = 9
                            new_entry = ({'Alias':[Name_list[number]] ,'Timestamp':[(str(periud_list[number]))[0:10]]
                                ,'Speed':[result[result.find('$ ')+1:result.find(' - ')]]
                                ,'StakeName': ['$' + result[result.find('Results:') + last_RB_spase:result.find('$')] + ' ' + result[result.find('$ ') + 2:result.find(' - ')]]
                                ,'Stake':[result[result.find('Results:')+9:result.find('$')]]
                                ,'Games':[result[result.find(' - ')+3:result.find(' spins')]]
                                , 'Profit': [result[result.find('Profit: ')+8:second_index]]})
                            df = pd.DataFrame(new_entry, columns=['Alias', 'Timestamp', 'Speed', 'StakeName', 'Stake', 'Games','Profit', 'RB'])
                            result_file = pd.concat([result_file, df], ignore_index=True, sort=False)
                            result_file.to_excel(f'file\\audit\\{name_file}_result.xlsx')
                            result = result[:result.find('Results:') ] + result[second_index + 2:]
                            result ='Results: '+ result
                            print( f'{result}_after')
                    else:
                        if "(1million)" in result[result.find('$ ') + 1:result.find(' - ')]:
                            first_index = result.find('$')
                            second_index = result.find('$', first_index + 1)
                            last_RB_spase = 0
                            if 'Results:  ' in result:
                                last_RB_spase = 10
                            elif 'Results: ' in result:
                                last_RB_spase = 9
                            if '' in result[result.find('(1million) ') + 10:result.find(' - ')]:
                                new_entry = (
                                {'Alias': [Name_list[number]], 'Timestamp': [(str(periud_list[number]))[0:10]]
                                    , 'Speed': ['Normal']
                                    ,'StakeName': ['$' + result[result.find('Results:') + last_RB_spase:result.find('$')] + ' (1M)']
                                    , 'Stake': [(result[result.find('Results:') + 9:result.find('$')])]
                                    , 'Games': [result[result.find(' - ') + 3:result.find(' spins')]]
                                    , 'Profit': [result[result.find('Profit: ') + 8:second_index]]
                                    ,
                                 'RB': [result[result.find('RB: 		Total: ') + 13:result.find('$		Chest:')]]})
                            else:

                                new_entry = ({'Alias': [Name_list[number]], 'Timestamp': [(str(periud_list[number]))[0:10]]
                                    , 'Speed':[result[result.find('$ ')+1:result.find(' - ')]]
                                    , 'StakeName': ['$' + result[result.find('Results:') + 10:result.find('$')] + ' (1M) ' + result[result.find('$ ') + 2:result.find(' - ')]]
                                    , 'Stake': [(result[result.find('Results:') + last_RB_spase:result.find('$')]) + '(1M)']
                                    , 'Games': [result[result.find(' - ') + 3:result.find(' spins')]]
                                    , 'Profit': [result[result.find('Profit: ')+8:second_index]]
                                    , 'RB': [result[result.find('RB: 		Total: ') + 13:result.find('$		Chest:')]]})
                            df = pd.DataFrame(new_entry,
                                              columns=['Alias', 'Timestamp', 'Speed',  'StakeName', 'Stake', 'Games','Profit', 'RB'])
                            result_file = pd.concat([result_file, df], ignore_index=True, sort=False)
                            result_file.to_excel(f'file\\audit\\{name_file}_result.xlsx')
                            result = result[:result.find('Results:')] + result[second_index + 2:]
                            result = 'Results: ' + result
                            print(f'{result}_after')
                        else:
                            first_index = result.find('$')
                            second_index = result.find('$', first_index + 1)
                            last_RB_spase = 0
                            if 'Results:  ' in result:
                                last_RB_spase = 10
                            elif 'Results: ' in result:
                                last_RB_spase =9
                            new_entry = ({'Alias': [Name_list[number]], 'Timestamp': [(str(periud_list[number]))[0:10]]
                                , 'Speed': [result[result.find('$ ')+1:result.find(' - ')]]
                                , 'StakeName': ['$' + result[result.find('Results: ') + last_RB_spase:result.find('$')] + ' ' + result[result.find('$ ') + 2:result.find(' - ')]]
                                , 'Stake': [result[result.find('Results:') + 9:result.find('$')]]
                                , 'Games': [result[result.find(' - ')+3:result.find(' spins')]]
                                , 'Profit': [result[result.find('Profit: ')+8:second_index]]
                                , 'RB': [result[result.find('RB: 		Total: ') + 13:result.find('$		Chest:')]]})
                            df = pd.DataFrame(new_entry, columns=['Alias', 'Timestamp', 'Speed', 'StakeName', 'Stake', 'Games','Profit', 'RB'])
                            result_file = pd.concat([result_file, df], ignore_index=True, sort=False)
                            result_file.to_excel(f'file\\audit\\{name_file}_result.xlsx')
                            result = result[:result.find('Results:')] + result[second_index + 2:]
                            result = 'Results: ' + result
                            print(f'{result}_after')
            print("dune")

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

def multiple_replace(page, dictionary):
    for i, j in dictionary.items():
        page = page.replace(i, j)
    return page

if __name__ == '__main__':
    myloop = asyncio.new_event_loop()
    myloop.create_task(dp.start_polling())
    myloop.run_forever()
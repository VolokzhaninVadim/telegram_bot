#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################################################################################
############################################## Импортируем необходимые модули и данные ########################################################
###############################################################################################################################################
# Для работы с SQL|
from sqlalchemy import create_engine

# Для работы с операционной сисемой 
import os

# Для работы с табличными данными
import pandas as pd

# Для работы telegram bot
import telebot 

# Получаем переменные окружения
PG_HOST = os.environ['PG_HOST']
PG_PASSWORD = os.environ['PG_PASSWORD']
LOGIN_NAME = os.environ['LOGIN_NAME']
TELEGRAM_TOKEN=os.environ['TELEGRAM_TOKEN']

# Создаем подключение к pg
engine = create_engine(f'postgres://{LOGIN_NAME}:{PG_PASSWORD}@{PG_HOST}:5432/{LOGIN_NAME}')

###############################################################################################################################################
############################################## Создаем приложение #############################################################################
###############################################################################################################################################

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode = None)

def balance_bd():
    """
    Получение текущего баланса c pg. 
    Вход: 
        нет.
    Выход: 
        result_dict(DataFrame) - таблица с балансом. 
    """
    query = """
            select 
                     id
                     ,balance
            from 
                    balance.balance
            order by
                    id
            """

    # Получаем данные из dwh
    balance_df = pd.read_sql(
        sql = query,
        con = engine
    )
    return balance_df

def current_balance():
    """
    Получение текущего баланса. 
    Вход: 
        нет.
    Выход: 
        result_dict(str) - текст с балансом. 
    """
    balance_df = balance_bd()
# Создадим словарь для обработки id
    id_text_dict = {2 : 'Жена телефон', 3 : 'Интернет', 4 : 'Мой телефон', 5 : 'Основной счет', 6 : 'Копилка', 7 : 'Рабство'}
# Подменим id на текст
    balance_df['id'] = balance_df['id'].apply(lambda x: id_text_dict[x])
    return balance_df.to_string(index = False, header = False)

# Передаем id 
ids = [774842658, 963475421] 

@bot.message_handler(content_types=['start', 'go', 'text'])
def get_text_messages(msg):
    """
    Получение баланса.
    Вход: 
        msg(str) - сообщение. 
    Выход:
        (str) - сообщение с балансом.
    """
    global ids
    if msg.from_user.id not in ids:
        bot.send_message(msg.chat.id, 'Ошибся адресом, дружок')
    else:
        if msg.text == "Баланс":
            bot.send_message(msg.from_user.id, current_balance())

bot.polling(none_stop = True, interval = 0)
# -*- coding: utf-8 -*-
import re

import telebot
from telebot import types

from sett import *
from dict import *
import pymysql

bot = telebot.TeleBot(KEY)


@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message.from_user.id, WELCOME_TEXT)
    con = pymysql.connect(HOST_NAME, USER_NAME, USER_PASS, SQL_NAME)
    cur = con.cursor()
    user_id = message.from_user.id
    isExist = cur.execute(f"SELECT * FROM users WHERE idusers = {user_id}")
    if not isExist:
        bank = 0.0
        cur.execute(f"INSERT INTO users VALUES ({user_id}, {bank}) ")
        for i, cat in enumerate(START_CAT):
            idcat = user_id * 10 + i
            sql = "INSERT INTO categories (idcategories, name, exp) VALUES (%s,%s,%s) "
            cur.execute(sql, (idcat, cat, 0.0))
            cur.execute(f"INSERT INTO user_cat VALUES ({user_id}, {idcat})")
        con.commit()
    con.close()


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.from_user.id, HELP_TEXT)


@bot.message_handler(commands=['bank'])
def bank_message(message):
    con = pymysql.connect(HOST_NAME, USER_NAME, USER_PASS, SQL_NAME)
    cur = con.cursor()
    user_id = message.from_user.id
    cur.execute(f"SELECT bank FROM users WHERE idusers = {user_id} ")
    cash = cur.fetchall()[0][0]
    cur.execute(f"""SELECT SUM(exp) FROM categories WHERE idcategories IN 
                    (SELECT cat_id FROM user_cat WHERE user_id = {user_id}) """)
    spend = cur.fetchall()[0][0]

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Изменить месячный заработок', callback_data='change_bank')
    keyboard.add(key_yes)

    bot.send_message(chat_id=message.from_user.id, text=BANK_TEXT.format(cash, spend).encode('utf-8'),
                     reply_markup=keyboard)
    cur.close()
    con.close()


@bot.callback_query_handler(func=lambda call: True)
def callback_func(call):
    if call.data == 'change_bank':
        markup = types.ForceReply(selective=False)
        bot.send_message(call.message.chat.id, "Введите новый банк:", reply_markup=markup)
        bot.register_next_step_handler(call.message, reply_bank)


def reply_bank(message):
    user_id = message.from_user.id
    new_bank = message.text
    con = pymysql.connect(HOST_NAME, USER_NAME, USER_PASS, SQL_NAME)
    cur = con.cursor()
    try:
        int(new_bank)
        cur.execute(f"UPDATE users SET bank = {new_bank} WHERE idusers = {user_id}")
        con.commit()
        bot.send_message(user_id, UPDATE_BANK)
    except TypeError:
        bot.send_message(user_id, "Ошибка, попробуй заного!")
        bot.clear_step_handler_by_chat_id(message.chat.id)
    finally:
        cur.close()
        con.close()


@bot.message_handler(commands=['exp'])
def exp_message(message):
    pass


@bot.message_handler(content_types=["text"])
def message_get(message):
    lines = re.split("\n", message.text)

    new_cat = []
    new_exp = []

    for line in lines:
        cat_match = re.findall(NEWCAT_PATT, line)
        exp_match = re.findall(NEWEXP_PATT, line)
        if cat_match:
            new_cat.append(cat_match)
        if exp_match:
            new_exp.append(exp_match)


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=5)

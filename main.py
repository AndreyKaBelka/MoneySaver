# -*- coding: utf-8 -*-
import re

import telebot

from sett import *
from dict import *
import pymysql

bot = telebot.TeleBot(KEY)

con = pymysql.connect(HOST_NAME, USER_NAME, USER_PASS, SQL_NAME)
cur = con.cursor()


@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message.from_user.id, WELCOME_TEXT)
    user_id = message.from_user.id
    bank = 0
    cur.execute(f"insert into users (idusers, bank) values ({user_id}, {bank}) ")
    con.commit()
    con.close()


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.from_user.id, HELP_TEXT)


@bot.message_handler(commands=['bank'])
def bank_message(message):
    pass


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

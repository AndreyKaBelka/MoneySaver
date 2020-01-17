import re

import telebot

import sett
from dict import *

bot = telebot.TeleBot(sett.KEY)


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


@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message.from_user.id, WELCOME_TEXT)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.from_user.id, HELP_TEXT)


@bot.message_handler(commands=['bank'])
def bank_message(message):
    pass


@bot.message_handler(commands=['exp'])
def exp_message(message):
    pass


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=5)

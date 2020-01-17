import telebot
import sett
from dict import *

bot = telebot.TeleBot(sett.KEY)


@bot.message_handler(content_types=["text"])
def message_get(message):
    pass


@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message.from_user.id, WELCOME_TEXT)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.from_user.id, HELP_TEXT)


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=5)

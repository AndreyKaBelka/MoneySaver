import telebot
import sett

bot = telebot.TeleBot(sett.KEY)


@bot.message_handler(content_types=["text"])
def message_get(message):
    print(message)
    if message.text == "Привет!":
        bot.send_message(message.from_user.id, "И тебе привет!")
    else:
        bot.send_message(message.from_user.id, "Не понимаю!")


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=5)
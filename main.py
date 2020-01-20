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
        cur.execute(f"INSERT INTO users VALUES ({user_id}, {bank}, {2}) ")
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

    bot.send_message(chat_id=message.from_user.id, text=BANK_TEXT.format(cash, spend, cash - spend).encode('utf-8'),
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
        float(new_bank)
        cur.execute(f"UPDATE users SET bank = {new_bank} WHERE idusers = {user_id}")
        con.commit()
        bot.send_message(user_id, UPDATE_BANK)
    except TypeError:
        bot.send_message(user_id, "Ошибка, попробуй заного!")
        bot.clear_step_handler_by_chat_id(message.chat.id)
    finally:
        cur.close()
        con.close()


@bot.message_handler(commands=['exp'])  # TODO: если значения exp одинаковые, бот выводит только одно значение
def exp_message(message):
    user_id = message.from_user.id
    con = pymysql.connect(HOST_NAME, USER_NAME, USER_PASS, SQL_NAME)
    cur = con.cursor()
    cur.execute(f"SELECT cat_id FROM user_cat WHERE user_id = {user_id}")
    rows = cur.fetchall()
    dict_vals = []
    for row in rows:
        cur.execute("SELECT * from categories WHERE idcategories = %s", (row[0]))
        vals = cur.fetchall()
        dict_vals.append((vals[0][1], vals[0][2]))
    dict_vals.sort(key=lambda val: val[1])
    text = EXP_TEXT
    for pair in dict_vals[::-1]:
        text += f"{pair[1]} - {pair[0]}\n"
    bot.send_message(user_id, text=text)
    cur.close()
    con.close()


@bot.message_handler(content_types=["text"])
def message_get(message):
    lines = re.split("\n", message.text)

    new_cats = []
    new_exps = []

    for line in lines:
        cat_match = re.findall(NEWCAT_PATT, line)
        exp_match = re.findall(NEWEXP_PATT, line)
        if cat_match:
            for match in cat_match:
                new_cats.append(match)
        if exp_match:
            for match in exp_match:
                new_exps.append(match)

    if new_exps or new_cats:
        con = pymysql.connect(HOST_NAME, USER_NAME, USER_PASS, SQL_NAME)
        cur = con.cursor()
        user_id = message.from_user.id
        if new_cats:
            cur.execute(f"SELECT cnt_cat FROM users WHERE idusers = {user_id}")
            count_cat = cur.fetchall()[0][0]
            for new_cat in new_cats:
                cat_id = user_id * 10 + count_cat
                cur.execute("INSERT INTO categories VALUES (%s, %s, %s)", (cat_id, new_cat, 0.0))
                cur.execute(f"INSERT INTO user_cat VALUES ({user_id}, {cat_id})")
                count_cat += 1
            cur.execute(f"UPDATE users SET cnt_cat = {count_cat} WHERE idusers = {user_id}")
            bot.send_message(user_id, "Новая категория добавлена!")

        if new_exps:
            for new_exp in new_exps:
                # TODO: Поиск по одному слову, а не по всем
                cur.execute("""UPDATE categories SET exp = exp + %s WHERE idcategories IN 
                                (SELECT cat_id FROM user_cat WHERE user_id = %s) AND name = %s""", (new_exp[0], user_id,
                                                                                                    new_exp[1]))
            bot.send_message(user_id, "Траты добавлены!")

        con.commit()
        cur.close()
        con.close()

    # TODO: Добавить функцию удаления категории


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=5)

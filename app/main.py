# -*- coding: utf-8 -*-
import re
import sys
import uuid

import telebot
from telebot import types

from app.dict import *
import pymysql
from app.console import Console
from app.sett import Settings as sett

console = Console(sys.argv)
console.canRun()
bot = telebot.TeleBot(sett.BOT_KEY)
con = pymysql.connect(sett.HOST_NAME, sett.USER_NAME, sett.USER_PASS, sett.SQL_NAME)
cur = con.cursor()


@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message.from_user.id, WELCOME_TEXT)
    user_id = message.from_user.id
    cur.execute(f"SELECT COUNT(user_id) FROM users WHERE user_id = {user_id}")
    is_exist = cur.fetchone()[0]
    print(1)
    if is_exist == 0:
        print(1)
        bank = 0.0
        cur.execute(f"INSERT INTO users VALUES ({user_id}, {bank}) ")
        con.commit()
        for cat in START_CAT:
            print(1)
            sql = "INSERT INTO categories VALUES (%s, %s)"
            cat_id = __generate_rand_int()
            cur.execute(sql, (cat_id, 0.0))
            con.commit()
            cur.execute(f"INSERT INTO user_cat VALUES ({user_id}, {cat_id})")
            for i, cat_key in enumerate(re.findall(NEWKYEWORDS, cat)):
                if i == 0:
                    cur.execute(f"INSERT INTO tags(cat_id, tag_desc, tag_main) VALUES ({cat_id}, '{cat_key}', TRUE)")
                else:
                    cur.execute(f"INSERT INTO tags(cat_id, tag_desc) VALUES ({cat_id}, '{cat_key}')")
        con.commit()
        print(1)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.from_user.id, HELP_TEXT)


@bot.message_handler(commands=['bank'])
def bank_message(message):
    user_id = message.from_user.id
    cur.execute(f"SELECT user_bank FROM users WHERE user_id = {user_id}")
    cash = cur.fetchone()[0]
    cur.execute(
        f"SELECT SUM(cat_exp) FROM categories JOIN user_cat ON user_cat.user_id = {user_id} AND categories.cat_id = user_cat.cat_id")
    spend = cur.fetchone()[0]

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Изменить месячный заработок', callback_data='change_bank')
    keyboard.add(key_yes)

    bot.send_message(chat_id=message.from_user.id, text=BANK_TEXT.format(cash, spend, cash - spend).encode('utf-8'),
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_func(call):
    if call.data == 'change_bank':
        markup = types.ForceReply(selective=False)
        bot.send_message(call.message.chat.id, "Введите новый банк:", reply_markup=markup)
        bot.register_next_step_handler(call.message, reply_bank)


def reply_bank(message):
    user_id = message.from_user.id
    new_bank = message.text
    try:
        float(new_bank)
        cur.execute(f"UPDATE users SET user_bank = {new_bank} WHERE user_id = {user_id}")
        con.commit()
        bot.send_message(user_id, UPDATE_BANK)
    except TypeError:
        bot.send_message(user_id, "Ошибка, попробуй заного!")
        bot.clear_step_handler_by_chat_id(message.chat.id)


@bot.message_handler(commands=['exp'])
def exp_message(message):
    user_id = message.from_user.id
    cur.execute(f"SELECT cat_id FROM user_cat WHERE user_id = {user_id}")
    rows = cur.fetchall()
    dict_vals = []
    for row in rows:
        cur.execute(
            f"SELECT cat_exp, tag_desc, tag_main FROM categories JOIN tags ON categories.cat_id = {row[0]} WHERE tags.cat_id = {row[0]}")
        vals = cur.fetchall()
        cat_string = f"%s%s"
        main_word = ""
        sub_main = ()
        for val in vals:
            if val[2]:
                main_word = val[1]
            else:
                sub_main += (val[1],)
        dict_vals.append((vals[0][0], (cat_string % (main_word, sub_main)).replace("'", "")))
    dict_vals.sort(key=lambda value: value[0])
    text = EXP_TEXT
    for pair in dict_vals[::-1]:
        text += f"{pair[0]} - {pair[1]}\n"
    bot.send_message(user_id, text=text)


@bot.message_handler(content_types=["text"])
def message_get(message):
    lines = re.split("\n", message.text)

    new_cats = []
    new_exps = []
    del_cats = []

    for line in lines:
        cat_match = re.findall(NEWCAT_PATT, line)
        exp_match = re.findall(NEWEXP_PATT, line)
        delcat_match = re.findall(DELCAT_PATT, line)
        if cat_match:
            for match in cat_match:
                new_cats.append(match)
        if exp_match:
            for match in exp_match:
                new_exps.append(match)
        if delcat_match:
            for match in delcat_match:
                del_cats.append(match)

    if new_exps or new_cats or del_cats:
        user_id = message.from_user.id
        add_newcat(user_id, new_cats)
        add_newexp(user_id, new_exps)
        del_categ(user_id, del_cats)

        con.commit()


def del_categ(user_id, del_cats):
    if del_cats:
        for del_cat in del_cats:
            if isexist(user_id, del_cat):
                cur.execute(f"SELECT cat_id FROM tags WHERE tag_desc LIKE '%{del_cat}%'")
                cat_id = cur.fetchone()[0]
                cur.execute(f"DELETE FROM categories WHERE cat_id = {cat_id}")
                con.commit()
        bot.send_message(user_id, "Категория удалена!")


def isexist(user_id, mods):
    for mod in mods:
        sql = f"""SELECT tag_desc FROM tags WHERE tag_desc LIKE '%{mod}%' AND cat_id IN 
                  (SELECT cat_id FROM user_cat WHERE user_id = {user_id})"""
        cur.execute(sql)
        if len(cur.fetchall()) > 0:
            return True
    return False


def add_newcat(user_id, new_cats):
    if new_cats:
        cur.execute(f"SELECT COUNT(cat_id) FROM user_cat WHERE user_id = {user_id}")
        count_cat = cur.fetchone()[0]
        if count_cat > MAX_CAT_COUNT:
            bot.send_message(user_id, "У вас слишком много категорий! Максимальное число - 10")
            return
        for new_cat in new_cats:
            key_words = re.findall(NEWKYEWORDS, new_cat)
            if not isexist(user_id, key_words):
                cat_id = __generate_rand_int()
                cur.execute("INSERT INTO categories VALUES (%s, %s)", (cat_id, 0.0))
                cur.execute(f"INSERT INTO user_cat VALUES ({user_id}, {cat_id})")
                for i, key_word in enumerate(key_words):
                    if i == 0:
                        cur.execute(f"INSERT INTO tags(cat_id, tag_desc, tag_main) VALUE ({cat_id},'{key_word}', TRUE)")
                    else:
                        cur.execute(f"INSERT INTO tags(cat_id, tag_desc) VALUE ({cat_id},'{key_word}')")
                con.commit()
            bot.send_message(user_id, "Новая категория добавлена!")


# :parameter new_exps[0] - new exp
# :parameter new_exps[1] - category name
def add_newexp(user_id, new_exps):
    if new_exps:
        for new_exp in new_exps:
            sql = "UPDATE categories SET cat_exp = cat_exp + {0} WHERE cat_id = (SELECT cat_id FROM tags WHERE tag_desc LIKE '%{2}%')".format(
                new_exp[0], user_id, new_exp[1])
            cur.execute(sql)
            con.commit()
        bot.send_message(user_id, "Траты добавлены!")


def __generate_rand_int() -> int:
    return int(str(uuid.uuid4().fields[-1])[:10])


if __name__ == "__main__":
    if console.canRun():
        bot.polling(none_stop=True, interval=5)
    else:
        raise SystemExit("Specify the config file using -f flag")

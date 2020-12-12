import sys
from os import listdir
from os.path import isfile, join

import pymysql

from app.sett import Settings as sett


def oper_with_folder(folder_path):
    my_path = sys.path[0] + folder_path

    con = pymysql.connect(sett.HOST_NAME, sett.USER_NAME, sett.USER_PASS, sett.SQL_NAME)
    cur = con.cursor()

    onlyfiles = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    for file in onlyfiles:
        with open(my_path + file, mode='r') as f:
            sql_script = f.read()
            try:
                for sql_command in sql_script.split(";")[:-1]:
                    cur.execute(sql_command + ";")
                con.commit()
            except pymysql.OperationalError as msg:
                print(f"Command skip {file}\n{msg}")

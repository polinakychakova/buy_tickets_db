import json
from typing import Optional

import pymysql


class UseDateBase:
    def __init__(self, config: dict):
        self.config = config

    def __enter__(self) -> Optional[pymysql.cursors.Cursor]:
        try:
            self.con = pymysql.connect(**self.config)
            self.cursor = self.con.cursor()
            return self.cursor
        except pymysql.err.OperationalError as err:
            if err.args[0] == 2003:
                print('Неверный формат host\n')
            if err.args[0] == 1045:
                print('Неверное имя пользователя или пароль\n')
            if err.args[0] == 1049:
                print('Не найдена база данных\n')
            print(err.args[1])
            return err
        except TypeError as err:
            print('Неверный формат конфига\n')
            return err

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        try:
            self.con.commit()
        except AttributeError as err:
            print('Не удалось подключиться к серверу\n')
            return err
        self.con.close()
        self.cursor.close()
        return True


def get_db_config() -> dict:
    try:
        with open("config.json", 'r') as config:
            db_config = json.load(config)
    except FileNotFoundError as err:
        if err.args[0] == 2:
            print('Такой файл не найден\n')
        print(err.args[1])
        exit(0)
    except json.decoder.JSONDecodeError as err:
        print('Не является файлом .json\n')
        exit(0)

    return db_config


def work_with_db(config: dict, sql: str) -> list:
    with UseDateBase(config) as cursor:
        try:
            cursor.execute(sql)
        except pymysql.err.ProgrammingError as err:
            if err.args[0] == 1146:
                print('Таблицы не существует\n')
            if err.args[0] == 1064:
                print('Неверный синтаксис запроса\n')
            print(err.args[1])
            return err
        except pymysql.err.OperationalError as err:
            if err.args[0] == 1054:
                print('Столбец не найден\n')
            print(err.args[1])
            return err

        schema = [column[0] for column in cursor.description]

        result = []

        for string in cursor.fetchall():
            result.append(dict(zip(schema, string)))
        return result


def make_update(config, sql):
    a = False
    with UseDateBase(config) as cursor:
        cursor.execute(sql)
        a = True
    return a


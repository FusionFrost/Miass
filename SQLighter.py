# -*- coding: utf-8 -*-
import sqlite3

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM music').fetchall()

    def insert_new_contacts(self, name, birth, user_id):
        """ Получаем все строки """
        with self.connection:
            # Запрос такого плана
            # query = 'insert into CONTACT_USERS(name, birth,user_id) values("Павел Шепшелевич","02.08.1994","1")'
            query = 'insert into CONTACT_USERS(name, birth,user_id) values("' + str(name) + '", "' + str(birth) +'", "' + str(user_id) + '")'

            return self.cursor.execute(query)

    def insert_new_user(self, telegram_id,first_name,user_name,last_name,language_code):
        """ Получаем все строки """
        with self.connection:
            # Запрос такого плана
            # query = 'insert into telegram_contact(telegram_id,first_name,user_name,last_name,language_code) values('61714776','Pavel','','Shepshelevich','ru-RU')'
            query = 'insert into telegram_contact(telegram_id, first_name, user_name, last_name, language_code) values("' + str(telegram_id) + '", "' + str(first_name) +'", "' + str(user_name) + '", "' + str(last_name) +'", "'+ str(language_code) + '")'
            return self.cursor.execute(query)

    def check_user_id(self, telegramId):
        """ Получаем все строки """
        with self.connection:
            # Запрос такого плана
            # query = 'insert into telegram_contact(telegram_id,first_name,user_name,last_name,language_code) values('61714776','Pavel','','Shepshelevich','ru-RU')'
            query = 'select telegram_id from telegram_contact where telegram_id = "' + str(telegramId) +'"'
            for row in self.cursor.execute(query):
                return True
            else:
                return False


    def select_single(self, rownum):
        """ Получаем одну строку с номером rownum """
        with self.connection:
            return self.cursor.execute('SELECT * FROM music WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM music').fetchall()
            return len(result)

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
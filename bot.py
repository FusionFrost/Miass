import config
import telebot
import os
import time
from SQLighter import SQLighter
import utils
import random
from telebot import types
import datetime
import requests
import csvEditor

import re                         # Для работы с регулярными выражениями

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Можно так
    # user = bot.get_me().__dict__['first_name']
    # Или так
    botName = bot.get_me().first_name           # Берем имя бота
    userName = message.from_user.first_name     # Берем имя пользователя
    # Приветсвие
    bot.send_message(message.chat.id, userName + ", Приветствую! Меня зовут " + botName + ". Чем я могу помочь?" )
    list_commands = "Список команд: \n/time - Текущее время\n/contacts - Управление контактами"
    bot.send_message(message.chat.id, list_commands)

    '''
    Валидация клиента в системе
    '''

    # Получаем данные
    userId = message.from_user.id                       # id пользователя в telegram
                                                        # Являетеся ли ботом? В документации есть is_bot
    firstName = message.from_user.first_name            # Имя пользователя
    userName = message.from_user.username               # Имя, отображающееся в telegram
    lastName = message.from_user.last_name              # Фамилия пользователя
    languageCode = message.from_user.language_code      # Используемый язык

    # Подключаемся к БД
    db_worker = SQLighter(config.database_contacts)

    # check_user_availible = True - Пользователь существует в системе
    #                      = False - Пользователь не существует в системе
    check_user_availible = db_worker.check_user_id(userId)                              # Проверяем существует ли пользователь в БД
    if(check_user_availible == False):
        db_worker.insert_new_user(userId, firstName, userName, lastName, languageCode)  # Выполняем запрос на регистрацию нового клиента в систему
    # Отсоединяемся от БД
    db_worker.close()

@bot.message_handler(commands=['contacts'])
def send_welcome_contacts(message):
    bot.send_message(message.chat.id, 'Пожалуйста, загрузите файл в формате GOOGLE CSV\nПодробнее: https://www.google.com/contacts/u/0/?cplus=0#contacts\nЕще->Экспорт->Выберите формат файла для экспорта->\
                                       Google CSV (для импорта в аккаунт Google)')

    # Загрузка документа
    @bot.message_handler(content_types=['document'])
    def downloadFile(message):
        userId = message.from_user.id
        a = message.document.file_id
        file_info = bot.get_file(a)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.token, file_info.file_path))
        csvEditor.csv_dict_reader(file.text, userId )
        bot.send_message(message.chat.id, "Файл успешно загружен.")

@bot.message_handler(commands=['time'])
def send_time_now(message):
    bot.send_message(message.chat.id, 'Доброе утро, сегодня {dt:%A} {dt:%B} {dt.day}, {dt.year}: '.format(dt = datetime.datetime.now()))

@bot.message_handler(commands=['Time'])
def send_welcome(message):
    a = True
    while a == True:
        now = datetime.datetime.now()
        min = now.minute
        if min == 47:
            bot.send_message(message.chat.id, 'Доброе утро, {}'.format(min))
            a = False

@bot.message_handler(commands=['test'])
def find_file_ids(message):
    for file in os.listdir('music/'):
        if file.split('.')[-1] == 'mp3':
            f = open('music/'+file, 'rb')
            msg = bot.send_voice(message.chat.id, f, None)
            # А теперь отправим вслед за файлом его file_id
            bot.send_message(message.chat.id, msg.voice.file_id, reply_to_message_id=msg.message_id)
        time.sleep(3)



# При любом вводе символов предлагать воспользоваться списком команд
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_all(message):
    user_text = message.text
    result = re.search( '\s*[Пп][Рр][Ии][Вв][Ее][Тт]\W*',user_text)
    if result:
        userName = message.from_user.first_name
        text = userName + ', Привет! Для начала работы с ботом введите команду /start'
        bot.send_message(message.chat.id, text)
    else:
        text = 'Для начала работы с ботом введите команду /start'
        bot.send_message(message.chat.id, text)



@bot.message_handler(commands=['game'])
def game(message):
    # Подключаемся к БД
    db_worker = SQLighter(config.database_name)
    # Получаем случайную строку из БД
    #row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    # Получаем случайную строку из БД
    row = db_worker.select_single(1)
    # Формируем разметку
    markup = utils.generate_markup(row[2], row[3])
    # Отправляем аудиофайл с вариантами ответа
    bot.send_voice(message.chat.id, row[1], reply_markup=markup)
    # Включаем "игровой режим"
    utils.set_user_game(message.chat.id, row[2])

    # Отсоединяемся от БД
    db_worker.close()

@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    # Если функция возвращает None -> Человек не в игре
    answer = utils.get_answer_for_user(message.chat.id)
    # Как Вы помните, answer может быть либо текст, либо None
    # Если None:
    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать игру, выберите команду /game')
    else:
        # Уберем клавиатуру с вариантами ответа.
        keyboard_hider = types.ReplyKeyboardRemove()
        # Если ответ правильный/неправильный
        if message.text == answer:
            bot.send_message(message.chat.id, 'Верно!', reply_markup=keyboard_hider)
        else:
            bot.send_message(message.chat.id, 'Увы, Вы не угадали. Попробуйте ещё раз!', reply_markup=keyboard_hider)
        # Удаляем юзера из хранилища (игра закончена)
        utils.finish_user_game(message.chat.id)

if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.polling(none_stop=True)
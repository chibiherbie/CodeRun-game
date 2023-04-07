import telebot
from .config import TELEGRAM_BOT_TOKEN, ID_ADMIN
from .message_texts import *
from .db import DataBase
from .util import get_user_from_sh, get_all_money_from_sh
from src.game import Game

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
db = DataBase()

interface_connect = None
game_info = Game()

json_sh = {
    'user': 'None',
    'command': 'None',
    'msg': 'None'
}


@bot.message_handler(commands=['start'])
def start(message):
    try:
        if not db.get_user(message.from_user.id):
            db.create_user(message.from_user.id, message.from_user.username)

        bot.send_message(message.chat.id, GREETINGS)

    except Exception as e:
        print(e)


@bot.message_handler(commands=['help'])
def help(message):
    try:
        if not db.get_user(message.from_user.id):
            db.create_user(message.from_user.id, message.from_user.username)

        bot.send_message(message.chat.id, HELP)
    except Exception as e:
        print(e)


# Смена имени для таблицы лидеров
@bot.message_handler(commands=['change_name'])
def change_name(message):
    try:
        if not db.get_user(message.from_user.id):
            db.create_user(message.from_user.id, message.from_user.username)

    except Exception as e:
        print(e)


# Вступить в игру
@bot.message_handler(commands=['game'])
def enter_game(message):
    try:
        if not db.get_user(message.from_user.id):
            db.create_user(message.from_user.id, message.from_user.username)

        if game_info.game_started:
            bot.send_message(message.chat.id, f'Игра уже идёт, дождись окончания, после чего введи новый код с монитора')
            return

        msg = bot.send_message(message.chat.id, 'Введи код игры, который видишь на экране')
        bot.register_next_step_handler(msg, enter_the_game)
    except Exception as e:
        print(e)


# Вступить в игру с кодом
def enter_the_game(message):
    try:
        if not db.get_user(message.from_user.id):
            db.create_user(message.from_user.id, message.from_user.username)

        if message.text == game_info.code_game:
            msg = {'user': message.chat.id, 'command': 'enter_the_game', 'name': message.from_user.username}
            interface_connect.message_update.emit(msg)

            db.enter_the_game(message.from_user.id)

            bot.send_message(message.chat.id, f'Ты успешно вошёл в игру!')
        else:
            bot.send_message(message.chat.id, f'Код введён не верно, попробуй ещё раз /game')

    except Exception as e:
        print(e)


# Управлять роботом
@bot.message_handler(commands=['robot'])
def robot(message):
    try:
        if not db.get_user(message.from_user.id):
            db.create_user(message.from_user.id, message.from_user.username)

        if not game_info.game_started:
            bot.send_message(message.chat.id, 'Игра ещё не началась! Надо ещё подождать)')
            return

        if not all(db.get_ingame(message.from_user.id)):
            print(db.get_ingame(message.from_user.id))
            bot.send_message(message.chat.id, 'Ты пока не можешь отправлять команды. Дождись окончания и отправь код комнаты')
            return

        msg = bot.send_message(message.chat.id, SEND_COMMANDS)
        bot.register_next_step_handler(msg, register_command)

    except Exception as e:
        print(e)


# Регистрация комманд робота
def register_command(message):
    """регистрирует команды игрока"""
    try:
        if not db.get_user(message.from_user.id):
            db.create_user(message.from_user.id, message.from_user.username)

        commands = [elem.strip().lower().replace('ё', 'е') for elem in message.text.split('\n')]
        for num, command in enumerate(commands):
            if command not in ['вверх', 'вниз', 'влево', 'вправо']:
                bot.send_message(message.chat.id, f'Команда не распознана\n №{num + 1} - {command}')
                bot.send_message(message.chat.id, f'Проверь правильность написания и отправь ещё раз /robot')
                return

        db.update_commands(message.from_user.id, ' '.join(commands))

        msg = {'user': message.chat.id, 'command': 'register_command',
               'code': ' '.join(commands)}

        interface_connect.message_update.emit(msg)

        bot.send_message(message.from_user.id, f'Команда принята, дождись окончание раунда')
    except Exception as e:
        print(e)


# Сколько у меня баллов
@bot.message_handler(commands=['coin'])
def get_coin(message):
    try:
        if not db.get_user(message.from_user.id):
            db.create_user(message.from_user.id, message.from_user.username)

        coin = db.get_coins(message.chat.id)
        bot.send_message(message.chat.id, f'На твоём счету - {coin}')
    except Exception as e:
        print(e)


# -------ADMIN---------

@bot.message_handler(commands=['admin'])
def admin_help(message):
    try:
        if message.from_user.id == ID_ADMIN:
            bot.send_message(message.chat.id, ADMIN_HELP)

    except Exception as e:
        print(e)


@bot.message_handler(commands=['create_code'])
def get_code(message):
    try:
        if message.from_user.id == ID_ADMIN:
            msg = {'user': 'ADMIN', 'command': 'create_code'}

            print(msg)

            interface_connect.message_update.emit(msg)

    except Exception as e:
        print(e)


@bot.message_handler(commands=['all_player'])
def get_all_money(message):
    try:
        if message.from_user.id == ID_ADMIN:
            users = get_all_money_from_sh()
            for user in users.items():
                db.set_money(user[0], user[1])
            bot.send_message(message.chat.id, 'Деньги все в казне')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['start_game'])
def start_game(message):
    try:
        if message.from_user.id == ID_ADMIN:
            msg = {'user': 'ADMIN', 'command': 'start_game'}

            print(msg)

            interface_connect.message_update.emit(msg)

            bot.send_message(ID_ADMIN, f'Start')

    except Exception as e:
        print(e)


@bot.message_handler(commands=['end_game'])
def end_game(message):
    try:
        if message.from_user.id == ID_ADMIN:
            msg = {'user': 'ADMIN', 'command': 'end_game'}

            print(msg)

            interface_connect.message_update.emit(msg)

            bot.send_message(ID_ADMIN, f'End')

    except Exception as e:
        print(e)


@bot.message_handler(commands=['clear'])
def clear(message):
    try:
        bot.send_message(message.chat.id, f'БД очищена')
        db.clear_tables()

    except Exception as e:
        print(e)


# Ответ на любое сообщение
@bot.message_handler(content_types=['text'])
def send_text(message):
    bot.send_message(message.chat.id, 'Прости, но я не знаю такой команды /help')


def start_tg(progressbarthread, game):
    global interface_connect, game_info

    print('Запуск бота')

    interface_connect = progressbarthread
    game_info = game

    bot.polling(none_stop=True)


if __name__ == "__main__":
    try:
        start_tg()
    except Exception as error:
        print('Ошибка при запуске -', error)

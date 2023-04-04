import telebot
from .config import TELEGRAM_BOT_TOKEN, ID_ADMIN
from .message_texts import *
from .db import DataBase
from .util import get_user_from_sh, get_all_money_from_sh


bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
db = DataBase()


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

        money = db.get_money(message.from_user.id)
        bot.send_message(message.chat.id, f'У тебя сейчас {money} SibCoin')
    except Exception as e:
        print(e)


# Управлять роботом
@bot.message_handler(commands=['robot'])
def pay(message):
    try:
        if not db.get_user(message.from_user.id):
            db.create_user(message.from_user.id, message.from_user.username)

        msg = bot.send_message(message.chat.id, SEND_COMMANDS)
        bot.register_next_step_handler(msg, register_command)

    except Exception as e:
        print(e)


# Регистрация комманд робота
def register_command(message):
    try:
        if not db.get_user(message.from_user.id):
            db.create_user(message.from_user.id, message.from_user.username)

        commands = [elem.strip().lower().replace('ё', 'е') for elem in message.text.split('\n')]
        for num, command in enumerate(commands):
            if command not in ['вперед', 'назад', 'влево', 'вправо']:
                bot.send_message(message.chat.id, f'Команда не распознана\n №{num + 1} - {command}')
                bot.send_message(message.chat.id, f'Проверь правильность написания и отправь ещё раз')

        db.update_commands(message.from_user.id, ' '.join(commands))
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


# ----ADMIN-----

@bot.message_handler(commands=['admin'])
def admin_help(message):
    try:
        if message.from_user.id == ID_ADMIN:
            bot.send_message(message.chat.id, ADMIN_HELP)

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


@bot.message_handler(commands=['start_gamen'])
def start_auction(message):
    global auction, pay_user
    try:
        if message.text == '/start_auction':
            bot.send_message(message.chat.id, 'Забыл отправить аргумент, отправь например так: /start_auction 10')
            return

        start_price = int(message.text.strip('/start_auction').strip())

        if message.from_user.id == ID_ADMIN:
            auction = True
            pay_user = ['123', start_price]

            all_user = db.get_all_user()

            for user in all_user:
                bot.send_message(user[1], f'Аукцион начался\n\nНачальная ставка - {start_price}')

            bot.send_message(ID_ADMIN, f'Start')

    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Что-то не то отправил...')


@bot.message_handler(commands=['end_auction'])
def end_auction(message):
    global auction, pay_user
    try:
        if message.from_user.id == ID_ADMIN:
            auction = False
            db.minus_money(pay_user[0], pay_user[1])

            all_user = db.get_all_user()

            for user in all_user:
                bot.send_message(user[1], f'Аукцион окончен\n\nКонечная ставка - {pay_user[1]}')

            bot.send_message(ID_ADMIN, f'{pay_user}')
            pay_user = ['123', 0]

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
    bot.send_message(message.chat.id, 'Прости, но я не знаю такой команды')


def start():
    bot.polling(none_stop=True)


if __name__ == "__main__":
    try:
        start()
    except Exception as error:
        print('Ошибка при запуске -', error)

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

        if not db.get_user_sh(message.from_user.id)[0]:
            msg = bot.send_message(message.chat.id, WHO_ARE_YOU)
            bot.register_next_step_handler(msg, send_email)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['help'])
def help(message):
    try:
        if not db.get_user_sh(message.from_user.id)[0]:
            bot.send_message(message.chat.id, 'Сначала авторизируйся /start')
            return

        bot.send_message(message.chat.id, HELP)
    except Exception as e:
        print(e)


def send_email(message):
    try:
        msg = bot.send_message(message.chat.id, 'Теперь введи пароль')
        bot.register_next_step_handler(msg, send_password, message.text)

    except Exception as e:
        print(e)


def send_password(message, email):
    try:
        if get_user_from_sh(email, message.text):
            money = db.get_money_for_reg(email)
            db.update_status_sh(message.from_user.id, email, message.text, money, True)
            bot.send_message(message.chat.id, 'Всё супер, ты в деле. Можешь ввести для деталей /help')
        else:
            bot.send_message(message.chat.id, 'Что-то не так, попробуй ешё раз')
            msg = bot.send_message(message.chat.id, 'Введи email')
            bot.register_next_step_handler(msg, send_email)

    except Exception as e:
        print(e)


@bot.message_handler(commands=['pay'])
def pay(message):
    global pay_user

    try:
        if not db.get_user_sh(message.from_user.id)[0]:
            bot.send_message(message.chat.id, 'Сначала авторизируйся /start')
            return

        if message.text == '/pay':
            bot.send_message(message.chat.id, 'Забыл отправить аргумент, отправь например так: /pay 10')
            return

        num = int(message.text.strip('/pay').strip())

        if not auction:
            bot.send_message(message.chat.id, 'Аукцион ещё не начался)')
            return

        if num % 5 != 0:
            bot.send_message(message.chat.id, 'Ставка не кратна 5')
            return

        if num <= pay_user[1]:
            bot.send_message(message.chat.id, f'Твоя ставка меньше нынешней ставки - {pay_user[1]}')
            return

        money = int(db.get_money(message.from_user.id))

        soon_money = money - num
        if soon_money < 0:
            bot.send_message(message.chat.id, f'Не достатчоно средств, у тебя - {money}')
            return

        pay_user = [message.from_user.id, num]

        all_user = db.get_all_user()
        for user in all_user:
            bot.send_message(user[1], f'Новая ставка - {num}')

    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Что-то не то отправил...')


@bot.message_handler(commands=['money'])
def money(message):
    try:
        money = db.get_money(message.from_user.id)
        bot.send_message(message.chat.id, f'У тебя сейчас {money} SibCoin')
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


@bot.message_handler(commands=['all_money'])
def get_all_money(message):
    try:
        if message.from_user.id == ID_ADMIN:
            users = get_all_money_from_sh()
            for user in users.items():
                db.set_money(user[0], user[1])
            bot.send_message(message.chat.id, 'Деньги все в казне')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['start_auction'])
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

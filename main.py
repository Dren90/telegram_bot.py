import telebot
from config import *
from extensions import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help',])
def menu(message: telebot.types.Message):
    text = "Чтобы начать работу, введите команду в следующем формате: \n<имя валюты> \
<в какую валюту необходимо перевести> \
<количество конвертируемой валюты>\n Увидеть список всех доступных валют - введите команду: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        val = message.text.split(' ')

        if len(val) > 3:
            raise ConvertionException(f'Слишком много параметров.')
        elif len(val) < 3:
            raise ConvertionException(" Вы ввели не все параметры")

        quote, base, amount = message.text.split(' ')
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as c:
        bot.reply_to(message, f'Ошибка пользователя\n{c}')
    except Exception as c:
        bot.reply_to(message, f'Не удалось обработать команду\n{c}')
    else:
        text = f'{total_base * float(amount)} {base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
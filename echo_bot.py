import telebot


access_token = '613496099:AAEBanfIyoR0o1ZOqXXco6oyxOe6RNTfPyI'
bot = telebot.TeleBot(access_token)

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)


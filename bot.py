from telegram.ext import Updater, CommandHandler

# Reemplaza 'TOKEN' con el token real de tu bot
TOKEN = 'TU_TOKEN_DE_TELEGRAM'

def start(update, context):
    update.message.reply_text("¡Hola, soy tu bot!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
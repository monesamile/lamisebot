from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Reemplaza 'TOKEN' con el token real de tu bot
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'

def start(update: Update, context: CallbackContext):
    update.message.reply_text("¡Hola, soy tu bot!")

def main():
    # Configura el Updater sin usar polling
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Añadir el manejador del comando /start
    dispatcher.add_handler(CommandHandler('start', start))

    # Configura Webhooks (reemplaza con tu URL de servidor)
    updater.bot.set_webhook(url="https://tu-dominio.com/tu-path-de-webhook")
    
    # Inicia el servidor para recibir las actualizaciones
    updater.start_webhook(listen="0.0.0.0", port=80, url_path="tu-path-de-webhook")
    updater.idle()

if __name__ == '__main__':
    main()

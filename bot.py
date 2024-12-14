from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Lista de canales
CHANNEL_IDS = []

# Tu bot token
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'  # Sustituir con tu token


# Comando: /add <canal_id>
def add_canal(update: Update, context: CallbackContext):
    global CHANNEL_IDS
    if len(context.args) == 1:
        canal_id = context.args[0]
        if canal_id not in CHANNEL_IDS:
            CHANNEL_IDS.append(canal_id)
            update.message.reply_text(f"Canal agregado: {canal_id}")
        else:
            update.message.reply_text(f"El canal {canal_id} ya está en la lista.")
    else:
        update.message.reply_text("Por favor, proporciona un ID de canal válido. Uso: /add <canal_id>")


# Comando: /list
def list_canales(update: Update, context: CallbackContext):
    if CHANNEL_IDS:
        canales = "\n".join(CHANNEL_IDS)
        update.message.reply_text(f"Canales configurados:\n{canales}")
    else:
        update.message.reply_text("No hay canales configurados.")


# Función principal para iniciar el bot
def main():
    # Crear el Updater con el token de tu bot
    updater = Updater(token='TU_BOT_TOKEN', use_context=True)
    
    # Obtener el dispatcher para añadir los manejadores
    dp = updater.dispatcher

    # Comandos del bot
    dp.add_handler(CommandHandler('add', add_canal))
    dp.add_handler(CommandHandler('list', list_canales))

    # Iniciar el bot
    updater.start_polling()
    updater.idle()  # Mantener el bot funcionando

if __name__ == '__main__':
    main()


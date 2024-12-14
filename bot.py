from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables globales
CHANNEL_IDS = []  # Lista de IDs de canales

# Tu bot token
TOKEN = 'TU_BOT_TOKEN'  # Sustituir con tu token


# Comando: /add <canal_id>
async def add_canal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHANNEL_IDS
    if len(context.args) == 1:
        canal_id = context.args[0]
        if canal_id not in CHANNEL_IDS:
            CHANNEL_IDS.append(canal_id)
            await update.message.reply_text(f"Canal agregado: {canal_id}")
        else:
            await update.message.reply_text(f"El canal {canal_id} ya está en la lista.")
    else:
        await update.message.reply_text("Por favor, proporciona un ID de canal válido. Uso: /add <canal_id>")


# Comando: /list
async def list_canales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CHANNEL_IDS:
        canales = "\n".join(CHANNEL_IDS)
        await update.message.reply_text(f"Canales configurados:\n{canales}")
    else:
        await update.message.reply_text("No hay canales configurados.")


# Comando: /delete <canal_id>
async def delete_canal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHANNEL_IDS
    if len(context.args) == 1:
        canal_id = context.args[0]
        if canal_id in CHANNEL_IDS:
            CHANNEL_IDS.remove(canal_id)
            await update.message.reply_text(f"Canal eliminado: {canal_id}")
        else:
            await update.message.reply_text(f"El canal {canal_id} no está en la lista.")
    else:
        await update.message.reply_text("Por favor, proporciona un ID de canal válido. Uso: /delete <canal_id>")


# Función principal para iniciar el bot
async def main():
    # Inicializar la aplicación
    application = Application.builder().token(TOKEN).build()

    # Comandos del bot
    application.add_handler(CommandHandler('add', add_canal))
    application.add_handler(CommandHandler('list', list_canales))
    application.add_handler(CommandHandler('delete', delete_canal))

    # Iniciar el polling
    await application.run_polling()


if __name__ == '__main__':
    # Para evitar conflictos con el bucle de eventos, usamos esta forma
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(main())  # Ejecutamos la tarea principal del bot
    loop.run_forever()  # Mantiene el bucle de eventos en ejecución

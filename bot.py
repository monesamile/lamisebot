import logging
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables globales
CHANNEL_IDS = []  # Lista de IDs de canales

# Tu bot token
TOKEN = 'YOUR_BOT_TOKEN'  # Sustituir con tu token


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


# Comando: /SubirAnuncioPrueba1min
async def subir_anuncio_prueba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CHANNEL_IDS:
        bot = context.bot
        for canal_id in CHANNEL_IDS:
            try:
                # Enviar mensaje de texto
                mensaje = await bot.send_message(chat_id=canal_id, text="¡Hola Mundo! Este mensaje será borrado en 1 minuto.")

                # Enviar imagen de prueba
                with open("test_image.jpg", "rb") as image_file:  # Asegúrate de tener una imagen llamada "test_image.jpg"
                    imagen = await bot.send_photo(chat_id=canal_id, photo=image_file, caption="Esta es una imagen de prueba.")

                # Esperar 1 minuto y borrar mensaje e imagen
                await asyncio.sleep(60)
                await bot.delete_message(chat_id=canal_id, message_id=mensaje.message_id)
                await bot.delete_message(chat_id=canal_id, message_id=imagen.message_id)

            except Exception as e:
                logger.error(f"Error con el canal {canal_id}: {e}")
                await update.message.reply_text(f"Error con el canal {canal_id}: {e}")
    else:
        await update.message.reply_text("No hay canales configurados para enviar el anuncio.")


# Función principal
async def main():
    # Inicializar la aplicación
    application = Application.builder().token(TOKEN).build()

    # Comandos del bot
    application.add_handler(CommandHandler('add', add_canal))
    application.add_handler(CommandHandler('list', list_canales))
    application.add_handler(CommandHandler('delete', delete_canal))
    application.add_handler(CommandHandler('SubirAnuncioPrueba1min', subir_anuncio_prueba))

    # Ejecutar el bot usando un bucle no bloqueante
    await application.initialize()
    await application.start()
    print("Bot iniciado con éxito. Esperando comandos...")
    await application.updater.start_polling()  # Cambiado para no cerrar el bucle
    await asyncio.Event().wait()  # Esto mantiene el script en ejecución de forma indefinida


# Ejecutar la aplicación
if __name__ == '__main__':
    asyncio.run(main())

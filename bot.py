import logging
import asyncio
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables globales para almacenar el canal ID
CHANNEL_ID = None  # Inicialmente sin canal asignado

# Tu bot token
TOKEN = 'YOUR_BOT_TOKEN'  # Sustituir con tu token

# Función para agregar el canal con su ID
async def add_canal_con_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHANNEL_ID
    if len(context.args) == 1:
        CHANNEL_ID = context.args[0]  # Guardamos el ID del canal proporcionado
        await update.message.reply_text(f"Canal agregado con ID: {CHANNEL_ID}")
    else:
        await update.message.reply_text("Por favor, proporciona un ID de canal válido.")

# Función para enviar mensaje de prueba cada minuto
async def enviar_mensaje_prueba(bot: Bot):
    if CHANNEL_ID:
        try:
            await bot.send_message(CHANNEL_ID, "Este es un mensaje de prueba.")
            logger.info("Mensaje enviado con éxito.")
        except Exception as e:
            logger.error(f"Error al enviar el mensaje: {e}")
    else:
        logger.warning("No se ha configurado un canal para enviar mensajes.")

# Función para iniciar el bot y configurar el scheduler
async def main():
    # Inicializamos el bot y el scheduler
    application = Application.builder().token(TOKEN).build()
    bot = Bot(token=TOKEN)
    scheduler = AsyncIOScheduler()

    # Comando para agregar el canal
    add_canal_handler = CommandHandler('addCanalConID', add_canal_con_id)
    application.add_handler(add_canal_handler)

    # Agregar tarea al scheduler para enviar el mensaje cada minuto
    scheduler.add_job(enviar_mensaje_prueba, IntervalTrigger(minutes=1), args=[bot])

    # Iniciar el scheduler
    scheduler.start()

    # Comando para iniciar el bot
    await application.start_polling()

if __name__ == '__main__':
    asyncio.run(main())

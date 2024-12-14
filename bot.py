from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot, InputMediaPhoto
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import logging

# Habilitar el registro de logs para depurar
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Diccionario para almacenar los canales agregados
channels = {}

# Configuración de la imagen para el anuncio (puedes cambiarla)
image_path = 'path_a_tu_imagen.jpg'  # Coloca la ruta a la imagen que quieres enviar

# Función para agregar un canal
def add_channel(update, context):
    try:
        # Obtener el ID del canal desde el argumento
        channel_id = context.args[0]  # El primer argumento del comando /add
        if channel_id.isdigit():  # Verificar que el ID sea un número
            channel_id = int(channel_id)
            # Almacenar el canal en un diccionario con su ID
            channels[channel_id] = {'status': 'active'}
            update.message.reply_text(f"Canal {channel_id} añadido correctamente.")
        else:
            update.message.reply_text("Por favor, proporciona un ID de canal válido.")
    except IndexError:
        update.message.reply_text("Por favor, proporciona el ID del canal después del comando /add.")
    except Exception as e:
        update.message.reply_text(f"Hubo un error: {str(e)}")

# Función para listar los canales agregados
def list_channels(update, context):
    if channels:
        response = "Canales añadidos:\n"
        for channel_id in channels:
            response += f"- {channel_id}\n"
        update.message.reply_text(response)
    else:
        update.message.reply_text("No hay canales añadidos aún.")

# Función para eliminar un canal
def delete_channel(update, context):
    try:
        channel_id = int(context.args[0])  # El ID del canal
        if channel_id in channels:
            del channels[channel_id]
            update.message.reply_text(f"Canal {channel_id} eliminado correctamente.")
        else:
            update.message.reply_text("Canal no encontrado.")
    except IndexError:
        update.message.reply_text("Por favor, proporciona el ID del canal después del comando /delete.")
    except Exception as e:
        update.message.reply_text(f"Hubo un error: {str(e)}")

# Función para enviar el spam
def send_spam():
    for channel_id, info in channels.items():
        if info['status'] == 'active':
            # Enviar un mensaje con texto e imagen
            bot.send_photo(chat_id=channel_id, photo=open(image_path, 'rb'), caption="¡Este es un spam programado!")
            # Programar eliminación del mensaje después de 24 horas
            delete_time = datetime.now() + timedelta(hours=24)
            scheduler.add_job(delete_message, 'date', run_date=delete_time, args=[channel_id])

# Función para eliminar el mensaje
def delete_message(channel_id):
    # Aquí debes implementar la lógica para eliminar el mensaje
    # Necesitarías almacenar el message_id que has enviado y luego eliminarlo
    print(f"Mensaje en el canal {channel_id} eliminado.")

# Función para el anuncio de prueba
def subir_anuncio_prueba(update, context):
    for channel_id in channels:
        # Enviar un mensaje de prueba con "Hola Mundo" y una imagen
        bot.send_photo(chat_id=channel_id, photo=open(image_path, 'rb'), caption="Hola Mundo")
        # Programar la eliminación del mensaje después de 1 minuto
        delete_time = datetime.now() + timedelta(minutes=1)
        scheduler.add_job(delete_message, 'date', run_date=delete_time, args=[channel_id])

# Agregar la tarea programada para enviar el spam cada sábado a las 9:00 AM
scheduler = BackgroundScheduler()
scheduler.add_job(send_spam, 'cron', day_of_week='sat', hour=9, minute=0)
scheduler.start()

# Función principal para iniciar el bot
def main():
    global bot
    TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'  # Coloca tu token real de Telegram

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    bot = Bot(TOKEN)

    # Comandos
    dispatcher.add_handler(CommandHandler("add", add_channel))  # Añadir canal
    dispatcher.add_handler(CommandHandler("list", list_channels))  # Listar canales
    dispatcher.add_handler(CommandHandler("delete", delete_channel))  # Eliminar canal
    dispatcher.add_handler(CommandHandler("SubirAnuncioPrueba1min", subir_anuncio_prueba))  # Enviar anuncio de prueba

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

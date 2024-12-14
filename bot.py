
import logging
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.ext import Updater
import os

# Definición de tus IDs permitidos
ALLOWED_IDS = [6131021703, 1001520614779]  # Tu ID y el ID adicional

# Configuración del logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Guardar la imagen subida
image_path = None

# Función para verificar si el usuario tiene permisos
def is_allowed(update: Update):
    return update.message.from_user.id in ALLOWED_IDS

# Comando para comenzar
async def start(update: Update, context: CallbackContext):
    if is_allowed(update):
        await update.message.reply_text("¡Hola! ¿En qué puedo ayudarte hoy?")
    else:
        await update.message.reply_text("Lo siento, no tienes permisos para usar este bot.")

# Comando para agregar un canal
async def add_channel(update: Update, context: CallbackContext):
    if is_allowed(update):
        try:
            channel = context.args[0]
            # Guardar el canal en algún tipo de almacenamiento (base de datos, archivo, etc.)
            # Ejemplo de añadir a un archivo de texto:
            with open("channels.txt", "a") as file:
                file.write(f"{channel}\n")
            await update.message.reply_text(f"Canal {channel} agregado exitosamente.")
        except IndexError:
            await update.message.reply_text("Por favor, proporciona el nombre del canal.")
    else:
        await update.message.reply_text("No tienes permiso para agregar canales.")

# Comando para eliminar un canal
async def remove_channel(update: Update, context: CallbackContext):
    if is_allowed(update):
        try:
            channel = context.args[0]
            # Eliminar el canal de donde esté guardado
            with open("channels.txt", "r") as file:
                channels = file.readlines()
            with open("channels.txt", "w") as file:
                for line in channels:
                    if line.strip() != channel:
                        file.write(line)
            await update.message.reply_text(f"Canal {channel} eliminado.")
        except IndexError:
            await update.message.reply_text("Por favor, proporciona el nombre del canal.")
    else:
        await update.message.reply_text("No tienes permiso para eliminar canales.")

# Comando para enviar mensaje a los canales con imagen
async def send_message(update: Update, context: CallbackContext):
    if is_allowed(update):
        try:
            text = ' '.join(context.args)
            if image_path:
                # Enviar mensaje con imagen a los canales
                with open("channels.txt", "r") as file:
                    channels = file.readlines()
                for channel in channels:
                    channel = channel.strip()
                    try:
                        # Enviar el mensaje a cada canal
                        await context.bot.send_photo(chat_id=channel, photo=open(image_path, 'rb'), caption=text)
                        await update.message.reply_text(f"Mensaje enviado al canal {channel}.")
                    except Exception as e:
                        await update.message.reply_text(f"No se pudo enviar al canal {channel}: {str(e)}")
            else:
                await update.message.reply_text("No se ha configurado ninguna imagen para enviar.")
        except IndexError:
            await update.message.reply_text("Por favor, proporciona el mensaje que deseas enviar.")
    else:
        await update.message.reply_text("No tienes permiso para enviar mensajes a los canales.")

# Comando para editar imagen
async def edit_image(update: Update, context: CallbackContext):
    if is_allowed(update):
        if update.message.photo:
            # Guardar la foto recibida
            global image_path
            file = await update.message.photo[-1].get_file()
            image_path = f"images/{file.file_id}.jpg"
            await file.download(image_path)
            await update.message.reply_text("Imagen guardada exitosamente.")
        else:
            await update.message.reply_text("Por favor, sube una imagen para guardarla.")
    else:
        await update.message.reply_text("No tienes permiso para editar la imagen.")

# Comando de ayuda
async def help_command(update: Update, context: CallbackContext):
    if is_allowed(update):
        help_text = """
        Aquí tienes los comandos disponibles:
        /start - Inicia el bot.
        /add_channel [canal] - Agrega un canal.
        /remove_channel [canal] - Elimina un canal.
        /send_message [mensaje] - Envia un mensaje a los canales.
        /edit_image - Edita y guarda una imagen para enviarla.
        """
        await update.message.reply_text(help_text)
    else:
        await update.message.reply_text("No tienes permiso para acceder a la ayuda.")

# Manejo de errores
async def error(update: Update, context: CallbackContext):
    logger.warning(f"Update {update} caused error {context.error}")

# Función principal para arrancar el bot
def main():
    """Start the bot."""
    application = Application.builder().token('YOUR_TOKEN').build()

    # Registrar comandos
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('add_channel', add_channel))
    application.add_handler(CommandHandler('remove_channel', remove_channel))
    application.add_handler(CommandHandler('send_message', send_message))
    application.add_handler(CommandHandler('edit_image', edit_image))
    application.add_handler(CommandHandler('help', help_command))

    # Registrar el manejo de errores
    application.add_error_handler(error)

    # Ejecutar el bot
    application.run_polling()

if __name__ == '__main__':
    main()

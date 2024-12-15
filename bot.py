from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# Configuración básica
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'
ALLOWED_IDS = [6131021703, 1001520614779]  # Lista de IDs permitidos

# Carpeta donde se guardarán las imágenes subidas
IMAGE_DIR = "images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Lista de canales donde se enviarán los mensajes
canales = []

# Función para verificar si un usuario tiene permiso
def tiene_permiso(update: Update):
    return update.message.from_user.id in ALLOWED_IDS

# Comando /start - Muestra los comandos disponibles
async def start(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        await update.message.reply_text(
            "¡Hola, soy tu bot! Usa los siguientes comandos:\n"
            "/start - Muestra los comandos disponibles\n"
            "/addcanal - Añadir un canal\n"
            "/listacanales - Ver canales añadidos\n"
            "/editarimagen - Subir una imagen\n"
            "/testMensaje - Enviar un mensaje a los canales"
        )
    else:
        await update.message.reply_text("No tienes permisos para usar este bot.")

# Comando /addcanal - Añadir un canal
async def add_canal(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if context.args:
            canal_id = context.args[0]
            canales.append(canal_id)
            await update.message.reply_text(f"Canal {canal_id} añadido correctamente.")
        else:
            await update.message.reply_text("Por favor, proporciona un ID de canal. Ejemplo: /addcanal @miCanal")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

# Comando /listacanales - Mostrar todos los canales añadidos
async def listar_canales(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if canales:
            canales_str = "\n".join(canales)
            await update.message.reply_text(f"Canales añadidos:\n{canales_str}")
        else:
            await update.message.reply_text("No hay canales añadidos.")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

# Comando /editarimagen - Subir una imagen
# Comando /editarimagen - Subir una imagen
async def editar_imagen(update: Update, context: CallbackContext):
    if tiene_permiso(update):  # Verificar si el usuario tiene permisos
        if update.message.photo:  # Verificar si el mensaje contiene una foto
            photo = update.message.photo[-1]  # Obtener la imagen más grande (última en la lista)
            file = await photo.get_file()  # Obtener el archivo
            file_path = os.path.join(IMAGE_DIR, f"imagen_{update.message.message_id}.jpg")  # Establecer la ruta para guardar la imagen
            
            # Mensaje de depuración que se enviará por Telegram
            await update.message.reply_text("Recibiendo imagen...")  # Para depuración
            await file.download_to_drive(file_path)  # Descargar la imagen al servidor
            context.user_data['imagen_guardada'] = file_path  # Guardar la ruta en los datos del usuario
            
            # Confirmación de la imagen guardada
            await update.message.reply_text(f"Imagen recibida y guardada en: {file_path}")  # Confirmación
        else:
            await update.message.reply_text("Por favor, sube una imagen para guardar.")  # Mensaje si no hay imagen
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")  # Mensaje si el usuario no tiene permisos



# Comando /testMensaje - Enviar mensaje e imagen a los canales
async def test_mensaje(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if 'imagen_guardada' in context.user_data:
            image_path = context.user_data['imagen_guardada']
            with open(image_path, 'rb') as image_file:
                for canal_id in canales:
                    try:
                        await context.bot.send_photo(chat_id=canal_id, photo=image_file, caption="Holis amores")
                    except Exception as e:
                        await update.message.reply_text(f"No se pudo enviar el mensaje al canal {canal_id}: {e}")
                await update.message.reply_text("Mensaje e imagen enviados a los canales.")
        else:
            await update.message.reply_text("No se ha guardado ninguna imagen. Usa /editarimagen.")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

# Función para manejar el comando /help (mostrar ayuda)
async def help_command(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        await update.message.reply_text("¡Aquí tienes la ayuda! Usa los comandos que te he mostrado anteriormente.")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

# Comando /deletecanal - Eliminar un canal de la lista
async def delete_canal(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if context.args:
            canal_id = context.args[0]
            if canal_id in canales:
                canales.remove(canal_id)
                await update.message.reply_text(f"Canal {canal_id} eliminado.")
            else:
                await update.message.reply_text(f"Canal {canal_id} no encontrado.")
        else:
            await update.message.reply_text("Por favor, proporciona un ID de canal. Ejemplo: /deletecanal @miCanal")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

# Función principal que arranca el bot
def main():
    application = Application.builder().token(TOKEN).build()

    # Añadir los handlers de los comandos
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('addcanal', add_canal))
    application.add_handler(CommandHandler('listacanales', listar_canales))
    application.add_handler(CommandHandler('editarimagen', editar_imagen))
    application.add_handler(CommandHandler('testMensaje', test_mensaje))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('deletecanal', delete_canal))

    # Arrancar el bot con polling
    application.run_polling()

if __name__ == '__main__':
    main()



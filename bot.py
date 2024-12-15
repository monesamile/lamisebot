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
            "/subirimagen - Subir una imagen\n"
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

# Comando /subirimagen - Iniciar la subida de una imagen
async def subir_imagen(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        # Inicia el proceso pidiendo la imagen
        await update.message.reply_text("Por favor, sube una imagen para el anuncio.")
        context.user_data['esperando_imagen'] = True  # Indicamos que estamos esperando una imagen
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")  # Mensaje si no tienes permisos

# Este manejador se ejecutará cuando el usuario envíe una imagen
async def manejar_imagen(update: Update, context: CallbackContext):
    if 'esperando_imagen' in context.user_data and context.user_data['esperando_imagen']:
        if update.message.photo:  # Si el mensaje contiene una imagen
            print("Imagen recibida, procesando...")  # Depuración
            photo = update.message.photo[-1]  # Obtener la imagen más grande (última en la lista)
            file = await photo.get_file()  # Obtener el archivo
            file_path = os.path.join(IMAGE_DIR, f"imagen_{update.message.message_id}.jpg")  # Ruta donde guardamos la imagen
            await file.download_to_drive(file_path)  # Guardar la imagen

            # Guardar la ruta de la imagen en los datos del usuario
            context.user_data['imagen_guardada'] = file_path

            # Confirmación al usuario
            await update.message.reply_text("¡Ok! Tu imagen para el anuncio es:")

            # Mostrar la imagen en el chat
            with open(file_path, 'rb') as image_file:
                await update.message.reply_photo(image_file)

            # Desactivar la espera de la imagen
            context.user_data['esperando_imagen'] = False
        else:
            # Si el mensaje no contiene una imagen, pedirle que suba una
            await update.message.reply_text("Por favor, sube una imagen válida.")
    else:
        # Si no estamos esperando una imagen, ignora el mensaje
        await update.message.reply_text("No estoy esperando una imagen en este momento.")

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
            await update.message.reply_text("No se ha guardado ninguna imagen. Usa /subirimagen.")
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
    application.add_handler(CommandHandler('subirimagen', subir_imagen))
    application.add_handler(CommandHandler('testMensaje', test_mensaje))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('deletecanal', delete_canal))

    # Añadir el handler para manejar imágenes
    application.add_handler(MessageHandler(filters.PHOTO, manejar_imagen))

    # Arrancar el bot con polling
    application.run_polling()

if __name__ == '__main__':
    main()


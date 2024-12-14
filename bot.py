from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# Definir las ID permitidas
ALLOWED_IDS = [6131021703, 1001520614779]  # Añadimos la nueva ID aquí

# Reemplaza 'TOKEN' con el token real de tu bot
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'

# Carpeta donde se guardarán las imágenes
IMAGE_DIR = "images"

# Crear carpeta si no existe
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Guardar la imagen
async def guardar_imagen(update: Update, context: CallbackContext):
    """Guardar la imagen que el usuario suba."""
    if es_autorizado(update):
        # Obtener la imagen enviada
        photo = update.message.photo[-1]
        file = await photo.get_file()
        file_path = os.path.join(IMAGE_DIR, f"imagen_{update.message.message_id}.jpg")
        
        # Descargar la imagen al directorio
        await file.download_to_drive(file_path)
        
        # Guardar la ruta de la imagen en el contexto para usarla después
        context.user_data['imagen_guardada'] = file_path
        await update.message.reply_text("Imagen guardada correctamente. Ahora puedes enviarla con /testMensaje.")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

def es_autorizado(update: Update):
    """Verificar si el usuario está autorizado a ejecutar comandos."""
    return update.message.from_user.id in ALLOWED_IDS

async def start(update: Update, context: CallbackContext):
    """Muestra los comandos disponibles."""
    if es_autorizado(update):
        await update.message.reply_text(
            "¡Hola, soy tu bot! Los comandos disponibles son:\n"
            "/start - Muestra los comandos disponibles\n"
            "/addcanal - Añadir un canal privado\n"
            "/listacanales - Ver los canales añadidos\n"
            "/editarimagen - Enviar una imagen\n"
            "/testMensaje - Enviar un mensaje a todos los canales\n"
        )
    else:
        await update.message.reply_text("No tienes permisos para usar este bot.")

async def addcanal(update: Update, context: CallbackContext):
    """Añadir un canal a la lista de canales."""
    if es_autorizado(update):
        canal_id = context.args[0] if context.args else None
        if canal_id:
            # Aquí guardamos el canal
            await update.message.reply_text(f"Canal con ID {canal_id} añadido.")
        else:
            await update.message.reply_text("Por favor, proporciona un ID de canal.")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

async def listacanales(update: Update, context: CallbackContext):
    """Mostrar los canales añadidos."""
    if es_autorizado(update):
        # Aquí se mostrarían los canales guardados
        await update.message.reply_text("Lista de canales añadidos:")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

async def testMensaje(update: Update, context: CallbackContext):
    """Enviar mensaje a todos los canales añadidos."""
    if es_autorizado(update):
        # Comprobar si hay imagen guardada
        if 'imagen_guardada' in context.user_data:
            image_path = context.user_data['imagen_guardada']
            with open(image_path, 'rb') as image_file:
                # Enviar la imagen a los canales
                await update.message.reply_text("Enviando imagen y mensaje...")
                # Aquí puedes incluir el código para enviar la imagen y texto a los canales
                # Ejemplo de enviar a un canal (reemplaza con los canales añadidos)
                for canal_id in ["@canal1", "@canal2"]:  # Ejemplo de canales
                    await context.bot.send_photo(chat_id=canal_id, photo=image_file, caption="Holis amores")
            
            await update.message.reply_text(f"Mensaje e imagen enviados a los canales.")
        else:
            await update.message.reply_text("No se ha guardado ninguna imagen. Usa /editarimagen para cargar una.")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

def main():
    """Configuración y ejecución del bot."""
    application = Application.builder().token(TOKEN).build()

    # Añadir los manejadores de comandos y mensajes
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('addcanal', addcanal))
    application.add_handler(CommandHandler('listacanales', listacanales))
    application.add_handler(CommandHandler('testMensaje', testMensaje))
    
    # Manejar imágenes subidas por el usuario
    application.add_handler(MessageHandler(filters.PHOTO, guardar_imagen))

    # Iniciar el bot sin conflictos de "getUpdates"
    application.run_polling()

if __name__ == '__main__':
    main()




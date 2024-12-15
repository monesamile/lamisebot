from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# Configuración básica
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'
ALLOWED_IDS = [6131021703, 1001520614779]  # Lista de IDs permitidos (tu ID de usuario)

# Carpeta donde se guardarán las imágenes subidas
IMAGE_DIR = "images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Lista de canales y propietarios donde se enviarán los mensajes
canales = []  # Ejemplo: [{'canal_id': '@miCanal', 'propietario': '@propietario'}]

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
            "/modificarMensaje - Modificar el texto del mensaje\n"
            "/testMensaje - Enviar un mensaje a los canales"
        )
    else:
        await update.message.reply_text("No tienes permisos para usar este bot.")

# Comando /addcanal - Añadir un canal
async def add_canal(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if len(context.args) >= 2:
            canal_id = context.args[0]
            propietario = context.args[1]
            canales.append({'canal_id': canal_id, 'propietario': propietario})
            await update.message.reply_text(f"Canal {canal_id} añadido correctamente con propietario {propietario}.")
        else:
            await update.message.reply_text("Por favor, proporciona un ID de canal y un propietario. Ejemplo: /addcanal @miCanal @propietario")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

# Comando /listacanales - Mostrar todos los canales añadidos
async def listar_canales(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if canales:
            canales_str = "\n".join([f"Canal: {canal['canal_id']}, Propietario: {canal['propietario']}" for canal in canales])
            await update.message.reply_text(f"Canales añadidos:\n{canales_str}")
        else:
            await update.message.reply_text("No hay canales añadidos.")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

# Comando /subirimagen - Subir una imagen
async def subir_imagen(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        await update.message.reply_text("Por favor, sube una imagen para el anuncio.")
        context.user_data['esperando_imagen'] = True
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

# Este manejador se ejecutará cuando el usuario envíe una imagen
async def manejar_imagen(update: Update, context: CallbackContext):
    if 'esperando_imagen' in context.user_data and context.user_data['esperando_imagen']:
        if update.message.photo:  # Si el mensaje contiene una imagen
            photo = update.message.photo[-1]  # Obtener la imagen más grande (última en la lista)
            file = await photo.get_file()  # Obtener el archivo
            file_path = os.path.join(IMAGE_DIR, f"imagen_{update.message.message_id}.jpg")  # Ruta donde guardamos la imagen
            await file.download_to_drive(file_path)  # Guardar la imagen

            # Guardar la ruta de la imagen en los datos del usuario
            context.user_data['imagen_guardada'] = file_path

            # Confirmación al usuario
            await update.message.reply_text(
                f"¡Ok! Tu imagen para el anuncio es:\n"
                f"[Vista previa de la imagen]({file_path})", 
                parse_mode='Markdown'
            )
            # Mostrar la imagen en el chat
            with open(file_path, 'rb') as image_file:
                await update.message.reply_photo(image_file, caption="Aquí está la imagen que elegiste para el anuncio.")
            
            # Desactivar la espera de la imagen
            context.user_data['esperando_imagen'] = False
        else:
            await update.message.reply_text("Por favor, sube una imagen válida.")
    else:
        await update.message.reply_text("No estoy esperando una imagen en este momento.")

# Comando /modificarMensaje - Modificar el texto del mensaje
async def modificar_mensaje(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        # Pedir al usuario que envíe el texto que quiere usar
        await update.message.reply_text("Por favor, escribe el nuevo texto para el mensaje.")
        
        # Guardamos el estado para indicar que estamos esperando un texto
        context.user_data['esperando_texto'] = True
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

# Este manejador se ejecutará cuando el usuario envíe un texto
async def manejar_texto(update: Update, context: CallbackContext):
    if 'esperando_texto' in context.user_data and context.user_data['esperando_texto']:
        # Guardar el texto que el usuario envíe
        nuevo_texto = update.message.text
        context.user_data['texto_mensaje'] = nuevo_texto  # Guardamos el nuevo texto en los datos del usuario

        # Confirmación al usuario de que el texto fue guardado
        await update.message.reply_text(f"¡El texto se ha guardado correctamente!\nTexto: {nuevo_texto}")

        # Desactivamos la espera de texto
        context.user_data['esperando_texto'] = False
    else:
        # Si no estamos esperando texto, ignoramos el mensaje
        await update.message.reply_text("No estoy esperando un texto en este momento.")

# Comando /testMensaje - Enviar mensaje e imagen a los canales
async def test_mensaje(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if 'imagen_guardada' in context.user_data and 'texto_mensaje' in context.user_data:
            image_path = context.user_data['imagen_guardada']
            texto = context.user_data['texto_mensaje']
            with open(image_path, 'rb') as image_file:
                for canal in canales:
                    try:
                        await context.bot.send_photo(chat_id=canal['canal_id'], photo=image_file, caption=texto)
                    except Exception as e:
                        await update.message.reply_text(f"No se pudo enviar el mensaje al canal {canal['canal_id']}: {e}")
                await update.message.reply_text("Mensaje e imagen enviados a los canales.")
        else:
            await update.message.reply_text("No se ha guardado ninguna imagen o texto. Usa /subirimagen y /modificarMensaje.")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

# Comando /deletecanal - Eliminar un canal de la lista
async def delete_canal(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if context.args:
            canal_id = context.args[0]
            canal = next((c for c in canales if c['canal_id'] == canal_id), None)
            if canal:
                canales.remove(canal)
                await update.message.reply_text(f"Canal {canal_id} eliminado.")
            else:
                await update.message.reply_text(f"Canal {canal_id} no encontrado.")
        else:
            await update.message.reply_text("Por favor, proporciona un ID de canal. Ejemplo: /deletecanal @miCanal")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

# Manejador para detectar la eliminación de mensajes en los canales
async def on_message_deleted(update: Update, context: CallbackContext):
    if update.message and update.message.chat:
        # Buscar el canal que corresponde al ID de chat
        canal = next((c for c in canales if c['canal_id'] == update.message.chat.username), None)
        if canal:
            # Notificar al administrador sobre la eliminación del mensaje
            propietario = canal['propietario']
            await context.bot.send_message(
                chat_id=ALLOWED_IDS[0],  # Te notifica en tu chat (admin)
                text=f"El mensaje en el canal {canal['canal_id']} fue eliminado.\nPropietario del canal: {propietario}"
            )

# Función principal que arranca el bot
def main():
    application = Application.builder().token(TOKEN).build()

    # Añadir los handlers de los comandos
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('addcanal', add_canal))
    application.add_handler(CommandHandler('listacanales', listar_canales))
    application.add_handler(CommandHandler('subirimagen', subir_imagen))
    application.add_handler(CommandHandler('modificarMensaje', modificar_mensaje))
    application.add_handler(CommandHandler('testMensaje', test_mensaje))
    application.add_handler(CommandHandler('deletecanal', delete_canal))

    # Añadir manejadores para recibir texto e imágenes
    application.add_handler(MessageHandler(filters.PHOTO, manejar_imagen))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_texto))

    # Manejador para la eliminación de mensajes
    application.add_handler(MessageHandler(filters.StatusUpdate.MESSAGE_DELETED, on_message_deleted))

    # Arrancar el bot con polling
    application.run_polling()

if __name__ == '__main__':
    main()


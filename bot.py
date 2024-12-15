from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os
import asyncio

# Configuración básica
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'
ALLOWED_IDS = [6131021703, 1001520614779]  # Lista de IDs permitidos

# Carpeta donde se guardarán las imágenes subidas
IMAGE_DIR = "images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Lista de canales donde se enviarán los mensajes
canales = []
mensajes_enviados = []  # Para almacenar los mensajes enviados

# Lock para evitar la ejecución simultánea de la verificación
lock = asyncio.Lock()

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
            "/testMensaje - Enviar un mensaje a los canales\n"
            "/deletecanal - Eliminar un canal"
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
async def editar_imagen(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if update.message.photo:
            photo = update.message.photo[-1]
            file = await photo.get_file()
            file_path = os.path.join(IMAGE_DIR, f"imagen_{update.message.message_id}.jpg")
            await file.download_to_drive(file_path)
            context.user_data['imagen_guardada'] = file_path
            await update.message.reply_text("Imagen guardada correctamente.")
        else:
            await update.message.reply_text("Por favor, sube una imagen para guardar.")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

# Comando /testMensaje - Enviar mensaje e imagen a los canales
async def test_mensaje(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if 'imagen_guardada' in context.user_data and 'texto_mensaje' in context.user_data:
            image_path = context.user_data['imagen_guardada']
            texto = context.user_data['texto_mensaje']
            try:
                for canal_id in canales:
                    with open(image_path, 'rb') as image_file:
                        # Enviar imagen a cada canal individualmente
                        sent_message = await context.bot.send_photo(chat_id=canal_id, photo=image_file, caption=texto)
                        # Guardar el mensaje enviado
                        mensajes_enviados.append({'message_id': sent_message.message_id, 'chat_id': canal_id})
            except Exception as e:
                await update.message.reply_text(f"No se pudo enviar el mensaje a los canales: {e}")
                return
            await update.message.reply_text("Mensaje e imagen enviados a los canales.")
        else:
            await update.message.reply_text("No se ha guardado ninguna imagen o texto. Usa /subirimagen y /modificarMensaje.")
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

# Función para verificar los mensajes eliminados
async def verificar_mensaje(context: CallbackContext):
    async with lock:  # Asegura que solo se ejecute una vez
        while True:
            await asyncio.sleep(60)  # Esperar un minuto
            for mensaje in mensajes_enviados:
                try:
                    # Intentar obtener el mensaje para ver si sigue existiendo
                    await context.bot.get_message(chat_id=mensaje['chat_id'], message_id=mensaje['message_id'])
                except Exception as e:
                    # Si el mensaje ha sido eliminado, se captura la excepción
                    print(f"Mensaje con ID {mensaje['message_id']} ha sido eliminado.")

                    # Obtener detalles del canal para conseguir el nombre de usuario
                    try:
                        chat = await context.bot.get_chat(mensaje['chat_id'])
                        canal_username = chat.username  # Obtener el @username del canal

                        # Notificar a las IDs verificadas
                        for id_verificada in ALLOWED_IDS:
                            mensaje_alerta = f"¡Alerta! El mensaje con ID {mensaje['message_id']} ha sido eliminado en el canal @{canal_username}."
                            try:
                                await context.bot.send_message(chat_id=id_verificada, text=mensaje_alerta)
                            except Exception as alert_error:
                                print(f"No se pudo enviar la alerta a la ID {id_verificada}: {alert_error}")
                    except Exception as chat_error:
                        print(f"No se pudo obtener el nombre de usuario del canal con ID {mensaje['chat_id']}: {chat_error}")

                    # Eliminar el mensaje de la lista
                    mensajes_enviados.remove(mensaje)
                    break  # Salir del bucle porque ya se procesó la eliminación del mensaje

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

    # Verificar los mensajes eliminados cada minuto
    application.job_queue.run_repeating(verificar_mensaje, interval=60, first=0)

    # Arrancar el bot con polling
    application.run_polling()

if __name__ == '__main__':
    main()


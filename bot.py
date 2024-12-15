from telegram import Update, ChatMember
from telegram.ext import Application, CommandHandler, CallbackContext, ChatMemberHandler, MessageHandler, filters
import os

# Configuración básica
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'
ALLOWED_IDS = [6131021703, 1001520614779]  # Lista de IDs permitidos

# Carpeta donde se guardarán las imágenes subidas
IMAGE_DIR = "images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Lista de canales y propietarios
canales = []  # Ejemplo: [{'canal_id': '@miCanal', 'propietario': '@propietario'}]
mensaje_personalizado = "Holis amores"

# Función para verificar si un usuario tiene permiso
def tiene_permiso(update: Update):
    return update.effective_user.id in ALLOWED_IDS

# Comando /start - Muestra los comandos disponibles
async def start(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        await update.message.reply_text(
            "¡Hola, soy tu bot! Usa los siguientes comandos:\n"
            "/start - Muestra los comandos disponibles\n"
            "/addcanal - Añadir un canal\n"
            "/listacanales - Ver canales añadidos\n"
            "/editarimagen - Subir una imagen\n"
            "/modificartexto - Cambiar el mensaje personalizado\n"
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

# Comando /editarimagen - Subir una imagen
async def editar_imagen(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if update.message.photo:
            photo = update.message.photo[-1]
            file = await photo.get_file()
            file_path = os.path.join(IMAGE_DIR, f"imagen_{update.message.message_id}.jpg")
            await file.download_to_drive(file_path)
            context.user_data['imagen_guardada'] = file_path
            # Enviar la imagen de vista previa antes de guardarla definitivamente
            with open(file_path, 'rb') as image_file:
                await update.message.reply_photo(photo=image_file, caption="Imagen guardada correctamente.")
        else:
            await update.message.reply_text("Por favor, sube una imagen para guardar.")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

# Comando /modificartexto - Cambiar el mensaje personalizado
async def modificar_texto(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if context.args:
            global mensaje_personalizado
            mensaje_personalizado = " ".join(context.args)
            await update.message.reply_text(f"Mensaje personalizado actualizado: {mensaje_personalizado}")
        else:
            await update.message.reply_text("Por favor, proporciona el nuevo texto. Ejemplo: /modificartexto Hola mundo")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

# Comando /testMensaje - Enviar mensaje e imagen a los canales
async def test_mensaje(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if 'imagen_guardada' in context.user_data:
            image_path = context.user_data['imagen_guardada']
            with open(image_path, 'rb') as image_file:
                for canal in canales:
                    try:
                        await context.bot.send_photo(chat_id=canal['canal_id'], photo=image_file, caption=mensaje_personalizado)
                    except Exception as e:
                        await update.message.reply_text(f"No se pudo enviar el mensaje al canal {canal['canal_id']}: {e}")
                await update.message.reply_text("Mensaje e imagen enviados a los canales.")
        else:
            await update.message.reply_text("No se ha guardado ninguna imagen. Usa /editarimagen.")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

# Manejador de cambios en el estado del bot en un canal
async def on_chat_member_update(update: Update, context: CallbackContext):
    chat_member_update = update.chat_member
    new_status = chat_member_update.new_chat_member.status
    old_status = chat_member_update.old_chat_member.status
    chat = chat_member_update.chat

    # Verificar si el bot fue eliminado del canal
    if old_status in ["member", "administrator"] and new_status in ["kicked", "left"]:
        canal = next((c for c in canales if c['canal_id'] == f"@{chat.username}"), None)
        if canal:
            propietario = canal['propietario']
            canales.remove(canal)  # Eliminar el canal de la lista
            # Notificar a todos los IDs permitidos
            for admin_id in ALLOWED_IDS:
                try:
                    await context.bot.send_message(
                        chat_id=admin_id,
                        text=(
                            f"🚨 **Notificación de eliminación** 🚨\n"
                            f"El canal {canal['canal_id']} ha sido eliminado o el bot fue expulsado.\n"
                            f"Propietario del canal: {propietario}"
                        ),
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    print(f"Error notificando al ID {admin_id}: {e}")

# Función principal que arranca el bot
def main():
    application = Application.builder().token(TOKEN).build()

    # Añadir los handlers de los comandos
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('addcanal', add_canal))
    application.add_handler(CommandHandler('listacanales', listar_canales))
    application.add_handler(CommandHandler('editarimagen', editar_imagen))
    application.add_handler(CommandHandler('modificartexto', modificar_texto))
    application.add_handler(CommandHandler('testMensaje', test_mensaje))

    # Manejador para cambios en el estado del bot en canales
    application.add_handler(ChatMemberHandler(on_chat_member_update, ChatMemberHandler.MY_CHAT_MEMBER))

    # Arrancar el bot con polling
    application.run_polling()

if __name__ == '__main__':
    main()

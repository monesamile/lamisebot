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

# Manejador para la detección de cambios o eliminación indirecta de mensajes (por ejemplo, cuando el chat se actualiza)
async def on_message_update(update: Update, context: CallbackContext):
    if update.message and update.message.chat:
        # Buscar el canal que corresponde al ID de chat
        canal = next((c for c in canales if c['canal_id'] == update.message.chat.username), None)
        if canal:
            # Notificar a todos los usuarios permitidos (ALLOWED_IDS)
            propietario = canal['propietario']
            for admin_id in ALLOWED_IDS:
                try:
                    await context.bot.send_message(
                        chat_id=admin_id,
                        text=(
                            f"🚨 **Notificación de cambio** 🚨\n"
                            f"Se detectó un cambio en el canal {canal['canal_id']}.\n"
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

    # Manejador para cambios en los mensajes (no eliminación directa, pero para detectar cambios)
    application.add_handler(MessageHandler(filters.Update.ALL, on_message_update))

    # Arrancar el bot con polling
    application.run_polling()

if __name__ == '__main__':
    main()



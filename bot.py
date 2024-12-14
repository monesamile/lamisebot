from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Definir las ID permitidas
ALLOWED_IDS = [6131021703, 1001520614779]  # Añadimos la nueva ID aquí

# Reemplaza 'TOKEN' con el token real de tu bot
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'

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

async def editarimagen(update: Update, context: CallbackContext):
    """Enviar una imagen."""
    if es_autorizado(update):
        # Lógica para enviar la imagen
        await update.message.reply_text("Imagen enviada.")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

async def testMensaje(update: Update, context: CallbackContext):
    """Enviar mensaje a todos los canales añadidos."""
    if es_autorizado(update):
        # Lógica para enviar mensaje a los canales
        await update.message.reply_text("Mensaje enviado a los canales.")
    else:
        await update.message.reply_text("No tienes permisos para usar este comando.")

def main():
    """Configuración y ejecución del bot."""
    application = Application.builder().token(TOKEN).build()

    # Añadir los manejadores de comandos
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('addcanal', addcanal))
    application.add_handler(CommandHandler('listacanales', listacanales))
    application.add_handler(CommandHandler('editarimagen', editarimagen))
    application.add_handler(CommandHandler('testMensaje', testMensaje))

    # Iniciar el bot sin conflictos de "getUpdates"
    application.run_polling()

if __name__ == '__main__':
    main()



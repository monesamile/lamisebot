from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Definir las ID permitidas
ALLOWED_IDS = [6131021703, 1001520614779]  # Añadimos la nueva ID aquí

# Reemplaza 'TOKEN' con el token real de tu bot
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'

def es_autorizado(update: Update):
    """Verificar si el usuario está autorizado a ejecutar comandos."""
    return update.message.from_user.id in ALLOWED_IDS

def start(update: Update, context: CallbackContext):
    """Muestra los comandos disponibles."""
    if es_autorizado(update):
        update.message.reply_text(
            "¡Hola, soy tu bot! Los comandos disponibles son:\n"
            "/start - Muestra los comandos disponibles\n"
            "/addcanal - Añadir un canal privado\n"
            "/listacanales - Ver los canales añadidos\n"
            "/editarimagen - Enviar una imagen\n"
            "/testMensaje - Enviar un mensaje a todos los canales\n"
        )
    else:
        update.message.reply_text("No tienes permisos para usar este bot.")

def addcanal(update: Update, context: CallbackContext):
    """Añadir un canal a la lista de canales."""
    if es_autorizado(update):
        canal_id = context.args[0] if context.args else None
        if canal_id:
            # Aquí guardamos el canal
            update.message.reply_text(f"Canal con ID {canal_id} añadido.")
        else:
            update.message.reply_text("Por favor, proporciona un ID de canal.")
    else:
        update.message.reply_text("No tienes permisos para usar este comando.")

def listacanales(update: Update, context: CallbackContext):
    """Mostrar los canales añadidos."""
    if es_autorizado(update):
        # Aquí se mostrarían los canales guardados
        update.message.reply_text("Lista de canales añadidos:")
    else:
        update.message.reply_text("No tienes permisos para usar este comando.")

def editarimagen(update: Update, context: CallbackContext):
    """Enviar una imagen."""
    if es_autorizado(update):
        # Lógica para enviar la imagen
        update.message.reply_text("Imagen enviada.")
    else:
        update.message.reply_text("No tienes permisos para usar este comando.")

def testMensaje(update: Update, context: CallbackContext):
    """Enviar mensaje a todos los canales añadidos."""
    if es_autorizado(update):
        # Lógica para enviar mensaje a los canales
        update.message.reply_text("Mensaje enviado a los canales.")
    else:
        update.message.reply_text("No tienes permisos para usar este comando.")

def main():
    """Configuración y ejecución del bot."""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Añadir los manejadores de comandos
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('addcanal', addcanal))
    dispatcher.add_handler(CommandHandler('listacanales', listacanales))
    dispatcher.add_handler(CommandHandler('editarimagen', editarimagen))
    dispatcher.add_handler(CommandHandler('testMensaje', testMensaje))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


from telegram.ext import Updater, CommandHandler

# Reemplaza con tu token de bot
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'
# ID del usuario autorizado
PERMITIDOS = [6131021703]

# Almacenamos los canales en un diccionario con ID como clave y nombre como valor
canales = {}

def check_user(update):
    """Verifica si el usuario está permitido."""
    return update.message.from_user.id in PERMITIDOS

def start(update, context):
    if check_user(update):
        update.message.reply_text("¡Hola, soy tu bot! Usa /help para ver los comandos.")
    else:
        update.message.reply_text("No tienes permiso para usar este bot.")

def add_canal(update, context):
    """Añadir un canal con ID y nombre."""
    if check_user(update):
        try:
            canal_id = context.args[0]
            canal_nombre = ' '.join(context.args[1:])
            # Guardamos el canal
            canales[canal_id] = canal_nombre
            update.message.reply_text(f"Canal '{canal_nombre}' con ID {canal_id} agregado.")
        except IndexError:
            update.message.reply_text("Por favor, usa el comando de la siguiente forma: /addcanal <ID> <Nombre del Canal>")
    else:
        update.message.reply_text("No tienes permiso para usar este comando.")

def list_canales(update, context):
    """Listar todos los canales almacenados."""
    if check_user(update):
        if canales:
            canal_list = "\n".join([f"ID: {canal_id}, Nombre: {nombre}" for canal_id, nombre in canales.items()])
            update.message.reply_text(f"Canales añadidos:\n{canal_list}")
        else:
            update.message.reply_text("No hay canales añadidos aún.")
    else:
        update.message.reply_text("No tienes permiso para usar este comando.")

def remove_canal(update, context):
    """Eliminar un canal por ID."""
    if check_user(update):
        try:
            canal_id = context.args[0]
            if canal_id in canales:
                canal_nombre = canales.pop(canal_id)
                update.message.reply_text(f"Canal '{canal_nombre}' con ID {canal_id} eliminado.")
            else:
                update.message.reply_text(f"No se encontró el canal con ID {canal_id}.")
        except IndexError:
            update.message.reply_text("Por favor, usa el comando de la siguiente forma: /removecanal <ID>")
    else:
        update.message.reply_text("No tienes permiso para usar este comando.")

def test_mensaje(update, context):
    """Enviar mensaje de prueba a todos los canales."""
    if check_user(update):
        if canales:
            for canal_id in canales:
                context.bot.send_message(chat_id=canal_id, text="¡Hola Mundo!")
            update.message.reply_text(f"Mensaje enviado a {len(canales)} canal(es).")
        else:
            update.message.reply_text("No hay canales añadidos.")
    else:
        update.message.reply_text("No tienes permiso para usar este comando.")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('addcanal', add_canal))
    dispatcher.add_handler(CommandHandler('listacanales', list_canales))
    dispatcher.add_handler(CommandHandler('removecanal', remove_canal))
    dispatcher.add_handler(CommandHandler('testmensaje', test_mensaje))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

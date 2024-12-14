from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Reemplaza con tu token de bot
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'
# ID del usuario autorizado
PERMITIDOS = [6131021703]

# Almacenamos los canales en un diccionario con ID como clave y nombre como valor
canales = {}

def check_user(update: Update):
    """Verifica si el usuario está permitido."""
    return update.message.from_user.id in PERMITIDOS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if check_user(update):
        await update.message.reply_text("¡Hola, soy tu bot! Usa /help para ver los comandos.")
    else:
        await update.message.reply_text("No tienes permiso para usar este bot.")

async def add_canal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Añadir un canal con ID y nombre."""
    if check_user(update):
        try:
            canal_id = context.args[0]
            canal_nombre = ' '.join(context.args[1:])
            # Guardamos el canal
            canales[canal_id] = canal_nombre
            await update.message.reply_text(f"Canal '{canal_nombre}' con ID {canal_id} agregado.")
        except IndexError:
            await update.message.reply_text("Por favor, usa el comando de la siguiente forma: /addcanal <ID> <Nombre del Canal>")
    else:
        await update.message.reply_text("No tienes permiso para usar este comando.")

async def list_canales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Listar todos los canales almacenados."""
    if check_user(update):
        if canales:
            canal_list = "\n".join([f"ID: {canal_id}, Nombre: {nombre}" for canal_id, nombre in canales.items()])
            await update.message.reply_text(f"Canales añadidos:\n{canal_list}")
        else:
            await update.message.reply_text("No hay canales añadidos aún.")
    else:
        await update.message.reply_text("No tienes permiso para usar este comando.")

async def remove_canal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Eliminar un canal por ID."""
    if check_user(update):
        try:
            canal_id = context.args[0]
            if canal_id in canales:
                canal_nombre = canales.pop(canal_id)
                await update.message.reply_text(f"Canal '{canal_nombre}' con ID {canal_id} eliminado.")
            else:
                await update.message.reply_text(f"No se encontró el canal con ID {canal_id}.")
        except IndexError:
            await update.message.reply_text("Por favor, usa el comando de la siguiente forma: /removecanal <ID>")
    else:
        await update.message.reply_text("No tienes permiso para usar este comando.")

async def test_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enviar mensaje de prueba a todos los canales."""
    if check_user(update):
        if canales:
            for canal_id in canales:
                await context.bot.send_message(chat_id=canal_id, text="¡Hola Mundo!")
            await update.message.reply_text(f"Mensaje enviado a {len(canales)} canal(es).")
        else:
            await update.message.reply_text("No hay canales añadidos.")
    else:
        await update.message.reply_text("No tienes permiso para usar este comando.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostrar ayuda con los comandos disponibles."""
    if check_user(update):
        help_text = """
        Comandos disponibles:
        /start - Saludo inicial
        /addcanal <ID> <Nombre del Canal> - Añadir un canal
        /listacanales - Listar los canales añadidos
        /removecanal <ID> - Eliminar un canal
        /testmensaje - Enviar un mensaje a los canales añadidos
        """
        await update.message.reply_text(help_text)
    else:
        await update.message.reply_text("No tienes permiso para usar este comando.")

def main():
    """Main function to set up the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('addcanal', add_canal))
    application.add_handler(CommandHandler('listacanales', list_canales))
    application.add_handler(CommandHandler('removecanal', remove_canal))
    application.add_handler(CommandHandler('testmensaje', test_mensaje))
    application.add_handler(CommandHandler('help', help_command))

    application.run_polling()

if __name__ == '__main__':
    main()


from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Reemplaza 'TOKEN' con el token real de tu bot
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'

# Variable global para almacenar los IDs de los canales añadidos
canales = []

# Función para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comandos = (
        "/start - Muestra este mensaje de bienvenida\n"
        "/addcanal <ID> - Añade un canal con su ID\n"
        "/listacanales - Muestra los canales añadidos"
    )
    await update.message.reply_text(f"¡Hola, soy tu bot! Aquí están los comandos disponibles:\n\n{comandos}")

# Función para agregar canales por ID
async def add_canal_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 1:
        canal_id = context.args[0]  # El primer argumento es el ID del canal
        canales.append(canal_id)  # Añadir a la lista de canales
        await update.message.reply_text(f"Canal con ID {canal_id} añadido exitosamente.")
    else:
        await update.message.reply_text("Por favor, proporciona el ID del canal después de /addcanal.")

# Función para mostrar los canales añadidos
async def mostrar_canales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if canales:
        canales_lista = "\n".join(canales)
        await update.message.reply_text(f"Canales añadidos:\n{canales_lista}")
    else:
        await update.message.reply_text("No hay canales añadidos aún.")

def main():
    # Crear la aplicación
    application = Application.builder().token(TOKEN).build()

    # Comandos
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('addcanal', add_canal_id))
    application.add_handler(CommandHandler('listacanales', mostrar_canales))  # Cambié el nombre aquí

    # Iniciar el polling
    application.run_polling()

if __name__ == '__main__':
    main()

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Token de tu bot
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'  # Sustituir con tu token

# Función para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola Mundo!")

# Función principal para iniciar el bot
async def main():
    # Crear el Application con el token de tu bot
    application = Application.builder().token(TOKEN).build()

    # Añadir el manejador de comandos
    application.add_handler(CommandHandler('start', start))

    # Iniciar el bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())



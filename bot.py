from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Lista de canales
CHANNEL_IDS = []

# Tu bot token
TOKEN = 'TU_BOT_TOKEN'  # Sustituir con tu token


# Comando: /add <canal_id>
async def add_canal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHANNEL_IDS
    if len(context.args) == 1:
        canal_id = context.args[0]
        if canal_id not in CHANNEL_IDS:
            CHANNEL_IDS.append(canal_id)
            await update.message.reply_text(f"Canal agregado: {canal_id}")
        else:
            await update.message.reply_text(f"El canal {canal_id} ya está en la lista.")
    else:
        await update.message.reply_text("Por favor, proporciona un ID de canal válido. Uso: /add <canal_id>")


# Comando: /list
async def list_canales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CHANNEL_IDS:
        canales = "\n".join(CHANNEL_IDS)
        await update.message.reply_text(f"Canales configurados:\n{canales}")
    else:
        await update.message.reply_text("No hay canales configurados.")


# Función principal para iniciar el bot
async def main():
    # Crear el Application con el token de tu bot
    application = Application.builder().token(TOKEN).build()

    # Añadir los manejadores de comandos
    application.add_handler(CommandHandler('add', add_canal))
    application.add_handler(CommandHandler('list', list_canales))

    # Iniciar el bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())



from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Reemplaza 'TOKEN' con el token real de tu bot
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'

# Lista para almacenar los IDs de los canales
canales_guardados = []

# Función para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola, soy tu bot!")

# Función para añadir un canal
async def add_canal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    canal_id = update.message.chat_id  # El chat_id del mensaje es el ID del canal
    if canal_id not in canales_guardados:
        canales_guardados.append(canal_id)
        await update.message.reply_text(f"Canal {canal_id} añadido con éxito.")
    else:
        await update.message.reply_text(f"El canal {canal_id} ya está guardado.")

# Función para listar los canales guardados
async def listar_canales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if canales_guardados:
        canales = "\n".join([str(canal) for canal in canales_guardados])
        await update.message.reply_text(f"Canales guardados:\n{canales}")
    else:
        await update.message.reply_text("No hay canales guardados.")

# Función para eliminar un canal
async def eliminar_canal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    canal_id = int(context.args[0])  # El ID del canal a eliminar se pasa como argumento
    if canal_id in canales_guardados:
        canales_guardados.remove(canal_id)
        await update.message.reply_text(f"Canal {canal_id} eliminado.")
    else:
        await update.message.reply_text(f"El canal {canal_id} no se encuentra en la lista.")

def main():
    # Crear la aplicación
    application = Application.builder().token(TOKEN).build()

    # Comandos disponibles
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('add', add_canal))  # Añadir un canal
    application.add_handler(CommandHandler('list', listar_canales))  # Listar los canales
    application.add_handler(CommandHandler('delete', eliminar_canal))  # Eliminar un canal

    # Comienza el polling
    application.run_polling()

if __name__ == '__main__':
    main()

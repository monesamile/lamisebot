from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Reemplaza 'TOKEN' con el token real de tu bot
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'

# Variable global para almacenar los IDs de los canales añadidos
canales = []

# Tu user_id o los user_ids permitidos
PERMITIDOS = [123456789, 987654321]  # Aquí debes poner tu user_id o los user_ids de las personas permitidas

# Función para verificar si el usuario tiene permisos
def verificar_permisos(update: Update) -> bool:
    user_id = update.message.from_user.id
    return user_id in PERMITIDOS

# Función para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if verificar_permisos(update):
        comandos = (
            "/start - Muestra este mensaje de bienvenida\n"
            "/addcanal <ID> - Añade un canal con su ID\n"
            "/listacanales - Muestra los canales añadidos\n"
            "/testMensaje - Envía un mensaje a todos los canales añadidos"
        )
        await update.message.reply_text(f"¡Hola, soy tu bot! Aquí están los comandos disponibles:\n\n{comandos}")
    else:
        await update.message.reply_text("No tienes permiso para usar este bot.")

# Función para agregar canales por ID
async def add_canal_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if verificar_permisos(update):
        if len(context.args) == 1:
            canal_id = context.args[0]  # El primer argumento es el ID del canal
            canales.append(canal_id)  # Añadir a la lista de canales
            await update.message.reply_text(f"Canal con ID {canal_id} añadido exitosamente.")
        else:
            await update.message.reply_text("Por favor, proporciona el ID del canal después de /addcanal.")
    else:
        await update.message.reply_text("No tienes permiso para ejecutar este comando.")

# Función para mostrar los canales añadidos
async def mostrar_canales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if verificar_permisos(update):
        if canales:
            canales_lista = "\n".join(canales)
            await update.message.reply_text(f"Canales añadidos:\n{canales_lista}")
        else:
            await update.message.reply_text("No hay canales añadidos aún.")
    else:
        await update.message.reply_text("No tienes permiso para ejecutar este comando.")

# Función para enviar el mensaje "¡Hola Mundo!" a todos los canales añadidos
async def test_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if verificar_permisos(update):
        if canales:
            for canal_id in canales:
                try:
                    # Enviar el mensaje al canal
                    await context.bot.send_message(chat_id=canal_id, text="¡Hola Mundo!")
                except Exception as e:
                    # Si ocurre un error al enviar el mensaje, lo imprimimos
                    print(f"Error al enviar mensaje al canal {canal_id}: {e}")
            await update.message.reply_text(f"Mensaje enviado a {len(canales)} canal(es).")
        else:
            await update.message.reply_text("No hay canales añadidos para enviar el mensaje.")
    else:
        await update.message.reply_text("No tienes permiso para ejecutar este comando.")

def main():
    # Crear la aplicación
    application = Application.builder().token(TOKEN).build()

    # Comandos
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('addcanal', add_canal_id))
    application.add_handler(CommandHandler('listacanales', mostrar_canales))  # Cambié el nombre aquí
    application.add_handler(CommandHandler('testMensaje', test_mensaje))  # Comando para enviar el mensaje

    # Iniciar el polling
    application.run_polling()

if __name__ == '__main__':
    main()

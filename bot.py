from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Reemplaza con tu token de bot
TOKEN = '7130748281:AAHsjLC4CgUPxyf0uBJ1I7InO7Nd6KlXOB4'

# Lista de canales
canales = {}

# Solo permitidos para interactuar con el bot
permitidos = [6131021703]  # Tu ID

# Verificar si el usuario tiene permiso
def tiene_permiso(update):
    user_id = update.message.from_user.id
    return user_id in permitidos

# Comando /start
async def start(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        await update.message.reply_text("¡Saludos, viajero! Soy Jaina, la maga de la tormenta. Estos son los comandos disponibles:\n"
                                       "/start - Inicia la interacción conmigo\n"
                                       "/addcanal - Añade un canal privado\n"
                                       "/listacanales - Muestra todos los canales añadidos\n"
                                       "/editarimagen - Enviar una imagen personalizada\n"
                                       "/testmensaje - Envía un mensaje a los canales añadidos\n"
                                       "/borrarcanal - Elimina un canal de la lista.")
    else:
        await update.message.reply_text("¡Oh! No tienes permiso para hablar conmigo, pero quizás algún día te lo conceda...")

# Comando /addcanal para añadir un canal
async def addcanal(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if context.args:
            canal_id = context.args[0]
            canal_nombre = " ".join(context.args[1:]) if len(context.args) > 1 else "Canal Desconocido"
            canales[canal_id] = canal_nombre
            await update.message.reply_text(f"¡El canal '{canal_nombre}' ha sido añadido con éxito!")
        else:
            await update.message.reply_text("¡Oh! Necesito el ID del canal para añadirlo.")
    else:
        await update.message.reply_text("¡Oh! No tienes permiso para hacer eso.")

# Comando /listacanales para mostrar los canales añadidos
async def listacanales(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if canales:
            mensaje = "Los canales añadidos son:\n"
            for canal_id, canal_nombre in canales.items():
                mensaje += f"- {canal_nombre} (ID: {canal_id})\n"
            await update.message.reply_text(mensaje)
        else:
            await update.message.reply_text("No hay canales añadidos todavía.")
    else:
        await update.message.reply_text("¡Oh! No tienes permiso para hacer eso.")

# Comando /borrarcanal para eliminar un canal
async def borrarcanal(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if context.args:
            canal_id = context.args[0]
            if canal_id in canales:
                del canales[canal_id]
                await update.message.reply_text(f"El canal con ID {canal_id} ha sido eliminado.")
            else:
                await update.message.reply_text(f"¡No encontré un canal con el ID {canal_id}!")
        else:
            await update.message.reply_text("¡Oh! Necesito el ID del canal para borrarlo.")
    else:
        await update.message.reply_text("¡Oh! No tienes permiso para hacer eso.")

# Comando /editarimagen para enviar una imagen personalizada
async def editarimagen(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        # Aquí subes tu imagen, por ejemplo: "imagen.jpg"
        await update.message.reply_text("Muy bien, querido. Aquí tienes la imagen que pediste.")
        # Reemplaza con el ID de la imagen que subes o el archivo correspondiente
        await update.message.reply_photo(photo=open('imagen.jpg', 'rb'), caption="Holis amores de Jaina.")
    else:
        await update.message.reply_text("¡Oh! No tienes permiso para hacer eso.")

# Comando /testmensaje para enviar un mensaje a los canales añadidos
async def testmensaje(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        mensaje = "Holis amores, esta es un mensaje de prueba."
        for canal_id in canales:
            try:
                await context.bot.send_message(chat_id=canal_id, text=mensaje)
                await update.message.reply_text(f"Mensaje enviado a {canales[canal_id]}.")
            except Exception as e:
                await update.message.reply_text(f"No pude enviar el mensaje a {canales[canal_id]}. Error: {str(e)}")
    else:
        await update.message.reply_text("¡Oh! No tienes permiso para hacer eso.")

def main():
    # Usamos Application de la versión 20+
    application = Application.builder().token(TOKEN).build()

    # Comandos
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('addcanal', addcanal))
    application.add_handler(CommandHandler('listacanales', listacanales))
    application.add_handler(CommandHandler('borrarcanal', borrarcanal))
    application.add_handler(CommandHandler('editarimagen', editarimagen))
    application.add_handler(CommandHandler('testmensaje', testmensaje))

    # Empezar el polling
    application.run_polling()

if __name__ == '__main__':
    main()



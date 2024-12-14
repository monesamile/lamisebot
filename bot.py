from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Reemplaza con tu token de bot
TOKEN = 'TU_TOKEN'

# Lista de canales
canales = {}

# Solo permitidos para interactuar con el bot
permitidos = [6131021703]  # Tu ID

# Verificar si el usuario tiene permiso
def tiene_permiso(update):
    user_id = update.message.from_user.id
    return user_id in permitidos

# Comando /start
def start(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        update.message.reply_text("¡Saludos, viajero! Soy Jaina, la maga de la tormenta. Estos son los comandos disponibles:\n"
                                  "/start - Inicia la interacción conmigo\n"
                                  "/addcanal - Añade un canal privado\n"
                                  "/listacanales - Muestra todos los canales añadidos\n"
                                  "/editarimagen - Enviar una imagen personalizada\n"
                                  "/testmensaje - Envía un mensaje a los canales añadidos\n"
                                  "/borrarcanal - Elimina un canal de la lista.")
    else:
        update.message.reply_text("¡Oh! No tienes permiso para hablar conmigo, pero quizás algún día te lo conceda...")

# Comando /addcanal para añadir un canal
def addcanal(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if context.args:
            canal_id = context.args[0]
            canal_nombre = " ".join(context.args[1:]) if len(context.args) > 1 else "Canal Desconocido"
            canales[canal_id] = canal_nombre
            update.message.reply_text(f"¡El canal '{canal_nombre}' ha sido añadido con éxito!")
        else:
            update.message.reply_text("¡Oh! Necesito el ID del canal para añadirlo.")
    else:
        update.message.reply_text("¡Oh! No tienes permiso para hacer eso.")

# Comando /listacanales para mostrar los canales añadidos
def listacanales(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if canales:
            mensaje = "Los canales añadidos son:\n"
            for canal_id, canal_nombre in canales.items():
                mensaje += f"- {canal_nombre} (ID: {canal_id})\n"
            update.message.reply_text(mensaje)
        else:
            update.message.reply_text("No hay canales añadidos todavía.")
    else:
        update.message.reply_text("¡Oh! No tienes permiso para hacer eso.")

# Comando /borrarcanal para eliminar un canal
def borrarcanal(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        if context.args:
            canal_id = context.args[0]
            if canal_id in canales:
                del canales[canal_id]
                update.message.reply_text(f"El canal con ID {canal_id} ha sido eliminado.")
            else:
                update.message.reply_text(f"¡No encontré un canal con el ID {canal_id}!")
        else:
            update.message.reply_text("¡Oh! Necesito el ID del canal para borrarlo.")
    else:
        update.message.reply_text("¡Oh! No tienes permiso para hacer eso.")

# Comando /editarimagen para enviar una imagen personalizada
def editarimagen(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        # Aquí subes tu imagen, por ejemplo: "imagen.jpg"
        update.message.reply_text("Muy bien, querido. Aquí tienes la imagen que pediste.")
        # Reemplaza con el ID de la imagen que subes o el archivo correspondiente
        update.message.reply_photo(photo=open('imagen.jpg', 'rb'), caption="Holis amores de Jaina.")
    else:
        update.message.reply_text("¡Oh! No tienes permiso para hacer eso.")

# Comando /testmensaje para enviar un mensaje a los canales añadidos
def testmensaje(update: Update, context: CallbackContext):
    if tiene_permiso(update):
        mensaje = "Holis amores, esta es un mensaje de prueba."
        for canal_id in canales:
            try:
                context.bot.send_message(chat_id=canal_id, text=mensaje)
                update.message.reply_text(f"Mensaje enviado a {canales[canal_id]}.")
            except Exception as e:
                update.message.reply_text(f"No pude enviar el mensaje a {canales[canal_id]}. Error: {str(e)}")
    else:
        update.message.reply_text("¡Oh! No tienes permiso para hacer eso.")

def main():
    # Usamos Updater con el nuevo modo
    updater = Updater(TOKEN)

    # Obtener el dispatcher para añadir los handlers
    dispatcher = updater.dispatcher

    # Comandos
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('addcanal', addcanal))
    dispatcher.add_handler(CommandHandler('listacanales', listacanales))
    dispatcher.add_handler(CommandHandler('borrarcanal', borrarcanal))
    dispatcher.add_handler(CommandHandler('editarimagen', editarimagen))
    dispatcher.add_handler(CommandHandler('testmensaje', testmensaje))

    # Empezar el polling
    updater.start_polling()

    # No dejar que el bot se detenga
    updater.idle()

if __name__ == '__main__':
    main()



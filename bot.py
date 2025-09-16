import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1001234567890  # замените на свой канал
RULES = "📌 ПРАВИЛА ЧАТА:\n1. Будьте вежливы\n2. Не спамьте\n3. Не разглашайте личную информацию"

bot = Bot(TOKEN)
application = Application.builder().token(TOKEN).build()
app = Flask(__name__)

# Обработчик постов канала
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post and update.channel_post.chat.id == CHANNEL_ID:
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=RULES,
            reply_to_message_id=update.channel_post.message_id
        )

application.add_handler(MessageHandler(filters.ChatType.CHANNEL, handle_channel_post))

# Webhook для Render
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Настройка webhook
url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/"
bot.set_webhook(url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # Например: https://yourapp.onrender.com
CHANNEL_ID = -1002891230799

RULES = """
ПРАВИЛА ЧАТА:
1. Будьте вежливы и уважительны к другим участникам.
2. Не спамьте и не рекламируйте без разрешения.
3. Не публикуйте запрещенные материалы.
"""

app = Flask(__name__)

async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:
        await context.bot.send_message(
            chat_id=update.channel_post.chat_id,
            text=RULES,
            message_thread_id=update.channel_post.message_id
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен!")

# Создаем приложение Telegram
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(MessageHandler(filters.ALL & filters.ChatType.CHANNEL, handle_channel_post))
application.add_handler(CommandHandler("start", start))

# Вебхук эндпоинт
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.create_task(application.update_queue.put(update))
    return "OK"

# Запуск вебхука при старте
if __name__ == "__main__":
    # Устанавливаем вебхук
    application.bot.set_webhook(f"{APP_URL}/{BOT_TOKEN}")
    print("Webhook установлен:", f"{APP_URL}/{BOT_TOKEN}")
    # Flask-сервер Render слушает порт из env
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

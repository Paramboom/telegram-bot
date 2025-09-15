import os
from flask import Flask, request, Response
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Создаем Flask-приложение
app = Flask(__name__)

# Токен бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID вашего канала (с минусом и 100 в начале)
CHANNEL_ID = -1002891230799

RULES = """
ПРАВИЛА ЧАТА:
1. Будьте вежливы и уважительны к другим участникам чата.
2. Не спамьте и не рекламируйте что-либо без разрешения администрации.
3. Не разглашайте личную информацию других участников без согласия.
4. Не обсуждайте политические или религиозные темы, если это может вызвать конфликты.
5. Обратитесь к администратору или другим участникам за помощью при вопросах.
6. Не распространяйте спам, вирусы или вредоносные программы.
7. Не публикуйте материалы, нарушающие законы или этические нормы.
8. Не нарушайте авторские права других людей или компаний.
9. Если вы не согласны с правилами чата, можете покинуть его.
"""

# Создаем ApplicationBuilder (Telegram)
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот, который комментирует новые посты.")

telegram_app.add_handler(CommandHandler("start", start))

# Обработчик постов из канала
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:
        try:
            await context.bot.send_message(
                chat_id=update.channel_post.chat_id,
                text=RULES,
                message_thread_id=update.channel_post.message_id
            )
        except Exception as e:
            print(f"Ошибка при отправке комментария: {e}")

telegram_app.add_handler(
    MessageHandler(filters.ALL & filters.ChatType.CHANNEL, handle_channel_post)
)

# Flask route для вебхука
@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.create_task(telegram_app.update_queue.put(update))
    return Response("OK", status=200)

# Автоматическая установка вебхука при старте
@app.before_first_request
def set_webhook():
    port = int(os.environ.get("PORT", 5000))
    url = os.environ.get("APP_URL")  # нужно указать URL вашего Render-сервиса
    webhook_url = f"{url}/webhook/{BOT_TOKEN}"
    telegram_app.bot.set_webhook(webhook_url)
    print(f"Webhook установлен: {webhook_url}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

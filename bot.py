import os
from flask import Flask, request, Response
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Настройки ---
BOT_TOKEN = os.getenv("BOT_TOKEN")           # Ваш токен бота
APP_URL = os.getenv("APP_URL")               # Ссылка на ваш Render-сервис, например: https://your-app.onrender.com
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"       # Путь для вебхука

# --- Flask приложение ---
app = Flask(__name__)

# --- Создание Application ---
application = ApplicationBuilder().token(BOT_TOKEN).build()

# --- Хэндлер команды /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот на вебхуках!")

application.add_handler(CommandHandler("start", start))

# --- Webhook endpoint для Telegram ---
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.create_task(application.update_queue.put(update))
    return Response("OK", status=200)

# --- Установка вебхука при старте Flask ---
@app.before_first_request
def set_webhook():
    webhook_url = f"{APP_URL}{WEBHOOK_PATH}"
    application.bot.set_webhook(webhook_url)
    print(f"Webhook установлен: {webhook_url}")

# --- Запуск приложения ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

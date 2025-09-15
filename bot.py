import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters

# --- Настройки ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/{BOT_TOKEN}"  # путь вебхука
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

# --- Flask приложение ---
app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

# --- Обработчики ---
async def handle_channel_post(update: Update, context):
    if update.channel_post:
        await context.bot.send_message(
            chat_id=update.channel_post.chat_id,
            text=RULES,
            message_thread_id=update.channel_post.message_id  # комментарий к посту
        )

dispatcher.add_handler(MessageHandler(filters.ALL & filters.ChatType.CHANNEL, handle_channel_post))

# --- Вебхук ---
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    """Обрабатываем обновления от Telegram"""
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

# --- Главная страница ---
@app.route("/")
def index():
    return "Bot is running!"

# --- Установка вебхука автоматически при старте Render ---
@app.before_first_request
def set_webhook():
    url = os.getenv("RENDER_EXTERNAL_URL")  # Render подставит публичный URL
    webhook_url = f"{url}{WEBHOOK_PATH}"
    bot.set_webhook(webhook_url)
    print(f"Webhook установлен: {webhook_url}")


import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

# ====== ДАННЫЕ ======
TOKEN = os.getenv("BOT_TOKEN")       # В Render: Environment Variable BOT_TOKEN
CHANNEL_ID = -1002891230799          # ID вашего канала
RULES = """📌 ПРАВИЛА ЧАТА:
1. Будьте вежливы и уважительны к другим участникам.
2. Не спамьте и не рекламируйте без разрешения.
3. Не разглашайте личную информацию других участников.
4. Не обсуждайте политические или религиозные темы.
5. Обратитесь к администратору за помощью при вопросах.
6. Не публикуйте вредоносные материалы.
7. Не нарушайте законы и авторские права.
8. Если не согласны с правилами, можете покинуть чат.
"""

# ====== Flask ======
app = Flask(__name__)
bot = Bot(TOKEN)
application = Application.builder().token(TOKEN).build()

# ====== Обработка сообщений канала ======
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post and update.channel_post.chat.id == CHANNEL_ID:
        # Отправляем комментарий к посту
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=RULES,
            reply_to_message_id=update.channel_post.message_id
        )

application.add_handler(MessageHandler(filters.ALL, handle_channel_post))

# ====== Webhook для Render ======
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "ok"

# ====== Настройка webhook ======
@app.before_request
def set_webhook():
    url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/"
    bot.set_webhook(url)

# ====== Запуск Flask ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

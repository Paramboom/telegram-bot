import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Данные
TOKEN = os.getenv("BOT_TOKEN")  # BOT_TOKEN задается в Environment Variables Render
CHANNEL_ID = -1002891230799     # твой канал
RULES = """📌 ПРАВИЛА ЧАТА:
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

# Flask app
app = Flask(__name__)
bot = Bot(TOKEN)
application = Application.builder().token(TOKEN).build()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает и готов комментировать посты!")

# Новый пост в канале
async def new_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post and update.channel_post.chat.id == CHANNEL_ID:
        chat_id = update.channel_post.chat.id
        message_id = update.channel_post.message_id
        await bot.send_message(chat_id=chat_id, text=RULES, reply_to_message_id=message_id)

# Хэндлеры
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.ChatType.CHANNEL, new_post))

# Flask endpoint для вебхука
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Установка вебхука
@app.before_first_request
def set_webhook():
    url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/"
    bot.set_webhook(url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

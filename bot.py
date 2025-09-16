import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# ====== ДАННЫЕ ======
TOKEN = os.getenv("BOT_TOKEN")  # Задай в Environment Variables на Render
CHANNEL_ID = -1002891230799     # Твой канал
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

# ====== FLASK И TELEGRAM ======
app = Flask(__name__)
bot = Bot(TOKEN)
application = Application.builder().token(TOKEN).build()

# ====== Хэндлеры ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает и готов комментировать посты!")

async def new_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post and update.channel_post.chat.id == CHANNEL_ID:
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=RULES,
            reply_to_message_id=update.channel_post.message_id
        )

# ====== Добавляем хэндлеры ======
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.ChatType.CHANNEL, new_post))

# ====== Webhook endpoint ======
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "ok"

# ====== Установка вебхука при старте ======
if "RENDER_EXTERNAL_HOSTNAME" in os.environ:
    url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/"
    bot.set_webhook(url)

# ====== Запуск Flask ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

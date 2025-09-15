import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_URL = os.getenv("BOT_URL")  # https://<твое-доменное-имя>
CHANNEL_ID = -1002891230799

RULES = """
ПРАВИЛА ЧАТА:
1. Будьте вежливы и уважительны к другим участникам чата.
2. Не спамьте и не рекламируйте что-либо без разрешения администрации.
3. Не разглашайте личную информацию других участников.
4. Не публикуйте материалы, нарушающие законы или этические нормы.
"""

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

def handle_channel_post(update: Update, context: CallbackContext):
    if update.channel_post:
        bot.send_message(
            chat_id=update.channel_post.chat_id,
            text=RULES,
            message_thread_id=update.channel_post.message_id
        )

dispatcher.add_handler(MessageHandler(filters.ALL & filters.ChatType.CHANNEL, handle_channel_post))

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return "OK"

@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    
    # Авто-настройка вебхука при старте
    webhook_url = f"{BOT_URL}/{BOT_TOKEN}"
    bot.delete_webhook()  # удаляем старый вебхук, если есть
    bot.set_webhook(url=webhook_url)
    print(f"Webhook set to {webhook_url}")
    
    app.run(host="0.0.0.0", port=port)

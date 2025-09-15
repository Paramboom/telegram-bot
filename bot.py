import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode
from flask import Flask, request, Response
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1002891230799  # ID твоего канала

RULES = """
*ПРАВИЛА ЧАТА:*
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

# Создаем Flask-приложение
app = Flask(__name__)

# Создаем Telegram-приложение
bot_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Обработчик новых постов в канале
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:
        try:
            await context.bot.send_message(
                chat_id=update.channel_post.chat.id,
                text=RULES,
                parse_mode=ParseMode.MARKDOWN,
                message_thread_id=update.channel_post.message_id  # комментарий к посту
            )
        except Exception as e:
            print("Ошибка при отправке комментария:", e)

bot_app.add_handler(MessageHandler(filters.ChatType.CHANNEL, handle_channel_post))

# Flask route для Telegram webhook
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    bot_app.update_queue.put(update)
    return Response("OK", status=200)

# Регистрация вебхука при старте
async def set_webhook():
    url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{BOT_TOKEN}"
    await bot_app.bot.set_webhook(url)
    print(f"Webhook установлен: {url}")

if __name__ == "__main__":
    # Устанавливаем вебхук перед запуском Flask
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_webhook())

    port = int(os.environ.get("PORT", 5000))
    print("Бот запущен с вебхуком...")
    app.run(host="0.0.0.0", port=port)

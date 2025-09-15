import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Токен бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID твоего канала
CHANNEL_ID = -1002891230799

RULES = """
ПРАВИЛА ЧАТА:
1. Будьте вежливы и уважительны к другим участникам.
2. Не спамьте и не рекламируйте без разрешения.
3. Не разглашайте личную информацию без согласия.
4. Не публикуйте материалы, нарушающие законы.
5. Если не согласны с правилами, можете покинуть чат.
"""

async def handle_new_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:  # ловим только новые посты в канале
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=RULES,
            message_thread_id=update.channel_post.message_id  # отправляем как комментарий к посту
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    # ловим все новые сообщения в канале (новые посты)
    app.add_handler(MessageHandler(filters.CHANNEL, handle_new_post))
    print("Бот запущен...")
    app.run_polling()

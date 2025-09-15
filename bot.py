import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Токен из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID твоего канала (с минусом и 100 в начале)
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

async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, что это новый пост в канале
    if update.channel_post:
        await context.bot.send_message(
            chat_id=update.channel_post.chat_id,  # отправляем в тот же канал
            text=RULES,
            message_thread_id=update.channel_post.message_id  # в комментарии к посту
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Ловим все сообщения из канала
    app.add_handler(MessageHandler(filters.ALL & filters.ChatType.CHANNEL, handle_channel_post))

    print("Бот запущен...")
    app.run_polling()

import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Твои правила чата
RULES = """ПРАВИЛА ЧАТА:

1. Будьте вежливы и уважительны к другим участникам чата. Не используи‌те оскорбительные или неприличные выражения.
2. Не спамьте и не рекламируи‌те что-либо в чате без разрешения администрации.
3. Не разглашаи‌те личную информацию других участников чата без их согласия.
4. Не обсуждаи‌те политические или религиозные темы в чате, если это может вызвать споры или конфликты.
5. Если у вас есть вопрос или проблема, обратитесь к администратору чата или к другим участникам, чтобы получить помощь.
6. Не используи‌те чат для распространения спама, вирусов или других вредоносных программ.
7. Не публикуи‌те материалы, которые нарушают законы или этические нормы.
8. Не нарушаи‌те авторские права других людеи‌ или компании‌.
9. Если вы не согласны с правилами чата, вы можете покинуть его.
"""

# Функция: когда в канале появляется новый пост
async def post_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:
        try:
            await context.bot.send_message(
                chat_id=update.channel_post.chat.id,
                text=RULES,
                reply_to_message_id=update.channel_post.message_id
            )
            logger.info("Правила отправлены под постом.")
        except Exception as e:
            logger.error(f"Ошибка при отправке правил: {e}")

def main():
    # Токен берём из переменной окружения (Render → Environment Variables)
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN не найден. Добавь его в Environment Variables на Render.")

    application = Application.builder().token(TOKEN).build()

    # Слушаем только новые посты в канале
    application.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, post_handler))

    logger.info("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()

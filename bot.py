from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Правила чата
RULES_TEXT = """ПРАВИЛА ЧАТА:

1. Будьте вежливы и уважительны к другим участникам чата. Не используи́те оскорбительные выражения.
2. Не спамьте и не рекламируйте что-либо в чате без разрешения администрации.
3. Не разглашайте личную информацию других участников чата без их согласия.
4. Не обсуждайте политические или религиозные темы в чате, если это может вызвать конфликты.
5. Если у вас есть вопрос или проблема, обратитесь к администратору чата.
6. Не используйте чат для распространения спама, вирусов или других вредоносных программ.
7. Не публикуйте материалы, нарушающие законы или этические нормы.
8. Не нарушайте авторские права других людей или компаний.
9. Если вы не согласны с правилами чата, вы можете покинуть его."""

# ID связанной группы обсуждений (где бот будет писать комментарии)
LINKED_GROUP_ID = -1001234567890  # замените на свой chat_id группы

async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Этот обработчик срабатывает на новый пост в канале
    и публикует комментарий в связанной группе.
    """
    if update.channel_post:
        # Можно добавить любые условия: например, только текстовые посты
        await context.bot.send_message(
            chat_id=LINKED_GROUP_ID,
            text=RULES_TEXT
        )
        logging.info(f"Комментарий к посту отправлен в группу {LINKED_GROUP_ID}")

if __name__ == "__main__":
    app = ApplicationBuilder().token("ВАШ_ТОКЕН_БОТА").build()

    # Обработчик новых постов в канале
    app.add_handler(MessageHandler(filters.CHANNEL, handle_channel_post))

    logging.info("Бот запущен...")
    app.run_polling()

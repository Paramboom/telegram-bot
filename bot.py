import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Здесь задаём правила чата (можешь заменить текст внутри кавычек)
CHAT_RULES = """
ПРАВИЛА ЧАТА:

1. Будьте вежливы и уважительны к другим участникам чата. Не используйте оскорбительные или неприличные выражения.
2. Не спамьте и не рекламируйте что-либо в чате без разрешения администрации.
3. Не разглашайте личную информацию других участников чата без их согласия.
4. Не обсуждайте политические или религиозные темы в чате, если это может вызвать споры или конфликты.
5. Если у вас есть вопрос или проблема, обратитесь к администратору чата или к другим участникам, чтобы получить помощь.
6. Не используйте чат для распространения спама, вирусов или других вредоносных программ.
7. Не публикуйте материалы, которые нарушают законы или этические нормы.
8. Не нарушайте авторские права других людей или компаний.
9. Если вы не согласны с правилами чата, вы можете покинуть его.
"""

# Функция-обработчик всех сообщений
async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        chat_id = update.effective_chat.id
        text = update.message.text
        print(f"Сообщение в чате {chat_id}: {text}")

        # Автоответ правилами
        await update.message.reply_text(CHAT_RULES)

def main():
    # Токен бота читаем из переменной окружения
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        print("Ошибка: не задан BOT_TOKEN в переменных окружения!")
        return

    # Создаём приложение
    app = ApplicationBuilder().token(TOKEN).build()

    # Обработчик ВСЕХ текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), on_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()

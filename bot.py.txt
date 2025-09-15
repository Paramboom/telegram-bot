import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Текст правил
RULES_TEXT = (
    "📜 Правила обсуждения:\n"
    "1. Вежливость и уважение.\n"
    "2. По теме поста.\n"
    "3. Реклама — только с разрешения.\n\n"
    "Спасибо за участие!"
)

async def on_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return
    if msg.sender_chat:  # сообщение от канала
        await msg.reply_text(RULES_TEXT)

async def main():
    TOKEN = os.getenv("TOKEN")  # токен берём из Environment Variable
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL & filters.ChatType.GROUPS, on_group_message))
    print("Бот запущен...")
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

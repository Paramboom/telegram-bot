import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from aiohttp import web

# === Текст правил чата ===
RULES_TEXT = """
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

# === Хэндлер команды /rules ===
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(RULES_TEXT)

# === aiohttp Web server (для Render) ===
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_webserver():
    port = int(os.environ.get("PORT", 10000))
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server started on port {port}")

# === Основная функция ===
async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Ошибка: не задан BOT_TOKEN в переменных окружения!")
        return

    # создаём приложение Telegram-бота
    application = Application.builder().token(token).build()

    # регистрируем команду
    application.add_handler(CommandHandler("rules", rules))

    # запускаем вебсервер и бота параллельно
    await start_webserver()
    print("Бот запущен...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

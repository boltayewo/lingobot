import asyncio
import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from admin import admin_router
from handlers import router as user_router


# Web server ping handler
async def handle_ping(request):
    return web.Response(text="Bot is running!")


async def main():
    # Loglarni sozlash
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_router(admin_router)
    dp.include_router(user_router)

    # Web serverni sozlash (cron-job.org va boshqa uptime monitorlar uchun)
    app = web.Application()
    app.router.add_route("*", "/", handle_ping)

    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    logging.info(f"Web server {port}-portda ishga tushdi.")

    try:
        # Eski pending xabarlarni o'chirib tashlash va pollingni boshlash
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        # Bot to'xtatilganda sessiyalar va web-serverni yopish
        await runner.cleanup()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
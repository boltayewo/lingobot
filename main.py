import asyncio
import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from admin import admin_router
# Agar tarjima uchun routeringiz bo'lsa, uni ham import qiling (masalan):
# from translator import user_router

async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_router(admin_router)
    # dp.include_router(user_router)  # Boshqa routeringiz bo'lsa, buni ham ulang

    # Render PORT'i uchun web serverni ishga tushirish
    app = web.Application()
    app.router.add_get("/", handle_ping)

    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    # Telegram bot polling rejimini boshlash
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
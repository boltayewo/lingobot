import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from db import init_db
from handlers import router
from admin import admin_router
from inline import inline_router


# Render.com portini tekshirishi uchun kichik veb-server javobi
async def handle(request):
    return web.Response(text="Bot muvaffaqiyatli ishlamoqda!")


async def main():
    logging.basicConfig(level=logging.INFO)

    # Bazani ishga tushirish
    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerni ulash
    dp.include_router(admin_router)
    dp.include_router(inline_router)
    dp.include_router(router)

    # Render ajratgan PORT'ni olish va veb-serverni ishga tushirish
    port = int(os.environ.get("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
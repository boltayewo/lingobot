import asyncio
import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from admin import admin_router

# GET, HEAD va boshqa barcha HTTP so'rovlariga javob beradi
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(admin_router)

    app = web.Application()
    # add_get o'rniga add_route("*", ...) qo'yildi
    app.router.add_route("*", "/", handle_ping)

    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
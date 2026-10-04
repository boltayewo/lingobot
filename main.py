import asyncio
import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher

# Config va Router'larni import qilish
from config import BOT_TOKEN
from admin import admin_router


# Agar sizda boshqa routerlar ham bo'lsa (masalan: user_router, translator_router), ularni ham shu yerda import qiling

# UptimeRobot ping yuborganda 200 OK qaytaruvchi handler
async def handle_ping(request):
    return web.Response(text="Bot is running!")


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_router(admin_router)
    # dp.include_router(boshqa_router)  # Boshqa routerlaringiz bo'lsa ularni ham shu yerga qo'shasiz

    # Render PORT'i uchun aiohttp web serverini ishga tushirish
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
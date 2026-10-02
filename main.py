import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from db import init_db
from handlers import router
from admin import admin_router
from inline import inline_router


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

    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
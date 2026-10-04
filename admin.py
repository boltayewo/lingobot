import random
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import ADMIN_ID
from db import (
    is_admin,
    get_user_stats,
    get_all_users,
    get_all_groups,
    add_admin,
    remove_admin,  # Bazadan adminni o'chirish uchun
    save_sent_ad,
    get_and_clear_last_ads
)

admin_router = Router()


class UnadminState(StatesGroup):
    waiting_for_id = State()


@admin_router.message(Command("botusers"))
async def bot_users_cmd(message: Message):
    if not is_admin(message.from_user.id, ADMIN_ID):
        return

    s = get_user_stats()
    msg = (
        f"👥 <b>User Statistics</b>\n\n"
        f"Total users: {s['total']}\n"
        f"Blocked (blocked the bot): {s['blocked']}\n\n"
        f"📅 New today: {s['today']}\n"
        f"📅 New this week: {s['week']}\n"
        f"📅 New this month: {s['month']}\n"
        f"📅 New this year: {s['year']}"
    )
    await message.answer(msg, parse_mode="HTML")


@admin_router.message(Command("botgroups"))
async def bot_groups_cmd(message: Message):
    if not is_admin(message.from_user.id, ADMIN_ID):
        return

    groups = get_all_groups()
    if not groups:
        await message.answer("Bot hali hech qaysi guruhga qo'shilmagan.")
        return

    res = "📋 <b>Guruhlar ro'yxati:</b>\n\n"
    for g_id, title in groups:
        res += f"• {title} (ID: {g_id})\n"
    await message.answer(res, parse_mode="HTML")


@admin_router.message(Command("addadmin"))
async def add_admin_cmd(message: Message):
    if not is_admin(message.from_user.id, ADMIN_ID):
        return

    args = message.text.split()
    if len(args) < 2:
        await message.answer("Foydalanish: `/addadmin USER_ID`", parse_mode="Markdown")
        return

    if not args[1].isdigit():
        await message.answer("Iltimos, to'g'ri raqamli ID kiriting!")
        return

    new_admin_id = int(args[1])
    add_admin(new_admin_id)
    await message.answer(f"Foydalanuvchi `{new_admin_id}` admin qilindi!", parse_mode="Markdown")


@admin_router.message(Command("unadmin"))
async def unadmin_cmd(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id, ADMIN_ID):
        return

    await state.set_state(UnadminState.waiting_for_id)
    await message.answer("Adminlikdan olib tashlamoqchi bo'lgan foydalanuvchining ID'sini yuboring:")


@admin_router.message(UnadminState.waiting_for_id)
async def process_unadmin_id(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id, ADMIN_ID):
        await state.clear()
        return

    user_input = message.text.strip()
    if not user_input.isdigit():
        await message.answer("Iltimos, faqat raqamlardan iborat foydalanuvchi ID'sini yuboring!")
        return

    target_id = int(user_input)
    remove_admin(target_id)
    await state.clear()
    await message.answer(f"ID: `{target_id}` bo'lgan foydalanuvchi adminlar ro'yxatidan olib tashlandi!", parse_mode="Markdown")


@admin_router.message(Command("rekads"))
async def send_ads_cmd(message: Message, bot: Bot):
    if not is_admin(message.from_user.id, ADMIN_ID):
        return

    if not message.reply_to_message:
        await message.answer("Reklama yuborish uchun xabarga reply qilib `/rekads` deb yozing!", parse_mode="Markdown")
        return

    users = get_all_users()
    count = 0
    for uid in users:
        try:
            sent = await message.reply_to_message.copy_to(chat_id=uid)
            save_sent_ad(uid, sent.message_id)
            count += 1
        except Exception:
            pass

    await message.answer(f"Reklama {count} ta userga yuborildi!")


@admin_router.message(Command("rekpeople"))
async def send_rek_people_cmd(message: Message, bot: Bot):
    if not is_admin(message.from_user.id, ADMIN_ID):
        return

    args = message.text.split()
    if len(args) < 2 or not message.reply_to_message:
        await message.answer("Foydalanish: Reklama xabariga reply qilib `/rekpeople 515` ko'rinishida yuboring.", parse_mode="Markdown")
        return

    if not args[1].isdigit():
        await message.answer("Iltimos, son kiriting!")
        return

    limit = int(args[1])
    users = get_all_users()
    target_users = random.sample(users, min(limit, len(users)))

    count = 0
    for uid in target_users:
        try:
            sent = await message.reply_to_message.copy_to(chat_id=uid)
            save_sent_ad(uid, sent.message_id)
            count += 1
        except Exception:
            pass

    await message.answer(f"Reklama tanlangan {count} ta random userga yuborildi!")


@admin_router.message(Command("deleteads"))
async def delete_ads_cmd(message: Message, bot: Bot):
    if not is_admin(message.from_user.id, ADMIN_ID):
        return

    ads = get_and_clear_last_ads()
    count = 0
    for uid, msg_id in ads:
        try:
            await bot.delete_message(chat_id=uid, message_id=msg_id)
            count += 1
        except Exception:
            pass

    await message.answer(f"Oxirgi yuborilgan reklamadan {count} tasi o'chirib tashlandi!")
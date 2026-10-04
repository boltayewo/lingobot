from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from db import add_user, set_user_lang, get_user_lang, add_group
from translator import translate_text
from config import ADMIN_ID

router = Router()

# ISO til kodlarini bayroq va 3 harfli qisqartmalarga moslash
LANG_COUNTRY_MAP = {
    'de': '🇩🇪 DEU',
    'en': '🏴󠁧󠁢󠁥󠁮󠁧󠁿 ENG',
    'ru': '🇷🇺 RUS',
    'uz': '🇺🇿 UZB',
    'tr': '🇹🇷 TUR',
    'fr': '🇫🇷 FRA',
    'es': '🇪🇸 ESP',
    'it': '🇮🇹 ITA',
    'zh-cn': '🇨🇳 CHN',
    'zh-tw': '🇨🇳 CHN',
    'ar': '🇸🇦 SAU',
    'af': '🇦🇫 AFG',
    'sq': '🇦🇱 ALB',
    'hy': '🇦🇲 ARM',
    'az': '🇦🇿 AZE',
    'be': '🇧🇾 BLR',
    'bg': '🇧🇬 BGR',
    'bs': '🇧🇦 BIH',
    'ca': '🇪🇸 ESP',
    'cs': '🇨🇿 CZE',
    'da': '🇩🇰 DNK',
    'el': '🇬🇷 GRC',
    'et': '🇪🇪 EST',
    'fa': '🇮🇷 IRN',
    'fi': '🇫🇮 FIN',
    'he': '🇮🇱 ISR',
    'hi': '🇮🇳 IND',
    'hr': '🇭🇷 HRV',
    'hu': '🇭🇺 HUN',
    'id': '🇮🇩 IDN',
    'is': '🇮🇸 ISL',
    'ja': '🇯🇵 JPN',
    'ka': '🇬🇪 GEO',
    'kk': '🇰🇿 KAZ',
    'km': '🇰🇭 KHM',
    'ko': '🇰🇷 KOR',
    'ky': '🇰🇬 KGZ',
    'lo': '🇱🇦 LAO',
    'lt': '🇱🇹 LTU',
    'lv': '🇱🇻 LVA',
    'mk': '🇲🇰 MKD',
    'mn': '🇲🇳 MNG',
    'ms': '🇲🇾 MYS',
    'ne': '🇳🇵 NPL',
    'nl': '🇳🇱 NLD',
    'no': '🇳🇴 NOR',
    'pl': '🇵🇱 POL',
    'pt': '🇵🇹 PRT',
    'ro': '🇷🇴 ROU',
    'sk': '🇸🇰 SVK',
    'sl': '🇸🇮 SVN',
    'sr': '🇷🇸 SRB',
    'sv': '🇸🇪 SWE',
    'tg': '🇹🇯 TJK',
    'th': '🇹🇭 THA',
    'tk': '🇹🇲 TKM',
    'uk': '🇺🇦 UKR',
    'ur': '🇵🇰 PAK',
    'vi': '🇻🇳 VNM'
}


class UserStates(StatesGroup):
    waiting_for_help = State()
    waiting_for_suggestion = State()


# Guruhga qo'shish tugmasini yaratuvchi yordamchi funksiya
def get_add_to_group_kb(bot_username: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="+ Guruhga qo'shish",
                url=f"https://t.me/{bot_username}?startgroup=true"
            )
        ]
    ])


@router.message(Command("start"))
async def start_cmd(message: Message):
    add_user(message.from_user.id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_lang_latin"),
            InlineKeyboardButton(text="🇺🇿 Ўзбекча", callback_data="set_lang_cyrillic")
        ]
    ])
    await message.answer("Tarjima tilini tanlang / Таржима тилини танланг:", reply_markup=kb)


@router.callback_query(F.data.startswith("set_lang_"))
async def set_lang_callback(call: CallbackQuery, bot: Bot):
    lang = call.data.split("_")[2]
    set_user_lang(call.from_user.id, lang)

    full_name = call.from_user.full_name
    bot_info = await bot.get_me()

    text = (
        f"Salom {full_name}! 👋\n"
        f"Menga istalgan tilda matn yuboring, men uni O'zbek tiliga tarjima qilaman.\n"
        f"Bot kanali: @Lingouzb"
    )
    await call.message.edit_text(text, reply_markup=get_add_to_group_kb(bot_info.username))


@router.message(Command("guruh"))
async def guruh_cmd(message: Message, bot: Bot):
    add_user(message.from_user.id)
    bot_info = await bot.get_me()
    text = (
        "Bu bot orqali siz guruhdagi matnlarni ham tarjima qilishingiz mumkin, "
        "Botni guruhga admin sifati qoshing va kerakli matnga /tarjima buyrugini yuboring ."
    )
    await message.answer(text, reply_markup=get_add_to_group_kb(bot_info.username))


@router.message(Command("donate"))
async def donate_cmd(message: Message):
    add_user(message.from_user.id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Donate", url="https://t.me/Devdonate")]
    ])
    await message.answer("@Devdonate donat kanali.", reply_markup=kb)


@router.message(Command("dev"))
async def dev_cmd(message: Message):
    add_user(message.from_user.id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Contact", url="https://t.me/boltayev")]
    ])
    await message.answer("Bot developer: @Boltayev", reply_markup=kb)


@router.message(Command("yordam"))
async def help_cmd(message: Message, state: FSMContext):
    add_user(message.from_user.id)
    await state.set_state(UserStates.waiting_for_help)
    await message.answer("Iltimos, muammoni yozib qoldiring. Biz uni tez orada ko'rib chiqamiz, rahmat!")


@router.message(Command("taklif"))
async def suggestion_cmd(message: Message, state: FSMContext):
    add_user(message.from_user.id)
    await state.set_state(UserStates.waiting_for_suggestion)
    await message.answer("Botni yaxshilash uchun taklifingizni yozib qoldiring 😊 Rahmat!")


@router.message(UserStates.waiting_for_help)
async def process_help(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    user = message.from_user
    username = f"@{user.username}" if user.username else "Mavjud emas"

    report_text = (
        f"📩 <b>Help request</b>\n"
        f"From: {user.full_name}\n"
        f"Username: {username}\n"
        f"ID: <code>{user.id}</code>\n"
        f"————————————————————\n\n"
        f"{message.text or message.caption or '[Media fayl]'}"
    )

    await bot.send_message(ADMIN_ID, report_text, parse_mode="HTML")
    await message.answer("Xabaringiz adminga yetkazildi!")


@router.message(UserStates.waiting_for_suggestion)
async def process_suggestion(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    user = message.from_user
    username = f"@{user.username}" if user.username else "Mavjud emas"

    report_text = (
        f"💡 <b>New suggestion</b>\n"
        f"From: {user.full_name}\n"
        f"Username: {username}\n"
        f"ID: <code>{user.id}</code>\n"
        f"————————————————————\n\n"
        f"{message.text or message.caption or '[Media fayl]'}"
    )

    await bot.send_message(ADMIN_ID, report_text, parse_mode="HTML")
    await message.answer("Taklifingiz adminga yetkazildi!")


# Admin guruhdan/chatdan reply orqali javob yuborganida
@router.message(F.chat.id == ADMIN_ID, F.reply_to_message)
async def admin_reply_handler(message: Message, bot: Bot):
    reply_msg = message.reply_to_message.text or message.reply_to_message.caption
    if not reply_msg or "ID:" not in reply_msg:
        return

    try:
        user_id = int(reply_msg.split("ID:")[1].split("\n")[0].strip())

        if "Help request" in reply_msg:
            prefix = "Yordam javobi admindan:\n"
        elif "New suggestion" in reply_msg:
            prefix = "Taklif bo'yicha javob admindan:\n"
        else:
            prefix = "Admindan javob:\n"

        await bot.send_message(user_id, f"{prefix}{message.text}")
        await message.reply("Javob foydalanuvchiga muvaffaqiyatli yetkazildi! ✅")
    except Exception as e:
        await message.reply(f"Xatolik yuz berdi: {e}")


# /tarjima buyrug'i tekshiruvi
@router.message(Command("tarjima"))
async def group_translate(message: Message, bot: Bot):
    if message.chat.type in ['group', 'supergroup']:
        add_group(message.chat.id, message.chat.title)

    target_text = None
    if message.reply_to_message:
        target_text = message.reply_to_message.text or message.reply_to_message.caption

    # Agar reply qilinmagan bo'lsa yoki shaxsiy chatda yuborilgan bo'lsa
    if not target_text:
        bot_info = await bot.get_me()
        text = "Bu buyrug'ni guruhda kerakli matnga reply qilib yuboring va bot o'sha matnni Tarjima qiladi."
        await message.reply(text, reply_markup=get_add_to_group_kb(bot_info.username))
        return

    translated, lang_code = await translate_text(target_text, target_script='latin')
    flag_str = LANG_COUNTRY_MAP.get(lang_code, f"🌐 {lang_code.upper()}")

    response = f"🔍 Asl tili: {flag_str}\n📝 Tarjima:\n{translated}"
    await message.reply(response)


# Shaxsiy chatlardagi barcha xabarlar tarjimasi
@router.message(F.chat.type == "private")
async def handle_private_messages(message: Message):
    add_user(message.from_user.id)

    text_to_translate = message.text or message.caption
    if not text_to_translate:
        return

    user_lang = get_user_lang(message.from_user.id)
    translated, lang_code = await translate_text(text_to_translate, target_script=user_lang)

    flag_str = LANG_COUNTRY_MAP.get(lang_code, f"🌐 {lang_code.upper()}")
    response = f"🔍 Asl tili: {flag_str}\n📝 Tarjima:\n{translated}"
    await message.reply(response)
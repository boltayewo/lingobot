from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from translator import translate_text

inline_router = Router()


@inline_router.inline_query()
async def inline_translate_handler(inline_query: InlineQuery):
    query = inline_query.query.strip()
    if not query:
        return

    translated, src = translate_text(query, target_script='latin')

    results = [
        InlineQueryResultArticle(
            id="1",
            title="Tarjima qilish (O'zbekcha)",
            description=translated,
            input_message_content=InputTextMessageContent(
                message_text=f"🔍 Asl tili: {src}\n📝 Tarjima:\n{translated}"
            )
        )
    ]
    await inline_query.answer(results, cache_time=1)
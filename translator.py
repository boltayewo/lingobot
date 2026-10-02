import asyncio
import translators as ts
from langdetect import detect

LATIN_TO_CYRILLIC = {
    'sh': 'ш', 'ch': 'ч', 'yo': 'ё', 'yu': 'ю', 'ya': 'я', 'ye': 'е', 'o\'': 'ў', 'g\'': 'ғ',
    'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 'z': 'з', 'i': 'и',
    'j': 'ж', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р',
    's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', 'x': 'х', 'h': 'ҳ', 'c': 'ц', 'q': 'қ', 'y': 'й'
}

def to_cyrillic(text: str) -> str:
    res = text
    for lat, cyr in LATIN_TO_CYRILLIC.items():
        res = res.replace(lat, cyr).replace(lat.capitalize(), cyr.upper())
    return res

def _do_translate(text: str):
    try:
        return ts.translate_text(query_text=text, translator='google', from_language='auto', to_language='uz', timeout=5)
    except Exception:
        try:
            return ts.translate_text(query_text=text, translator='bing', from_language='auto', to_language='uz', timeout=5)
        except Exception:
            return "Tarjima qilishda xatolik yuz berdi."

async def translate_text(text: str, target_script: str = 'latin') -> tuple[str, str]:
    # 1. Tilni aniqlash
    try:
        detected_lang = detect(text).lower()
    except Exception:
        detected_lang = 'en'

    # 2. Asinxron fonda tarjima qilish (bot qotib qolmasligi uchun)
    try:
        loop = asyncio.get_event_loop()
        translated = await loop.run_in_executor(None, _do_translate, text)
    except Exception:
        translated = "Tarjimada xatolik yuz berdi."

    if target_script == 'cyrillic':
        translated = to_cyrillic(translated)

    return translated, detected_lang
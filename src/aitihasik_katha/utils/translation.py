import asyncio

from google.cloud import translate_v2
from googletrans import Translator

from aitihasik_katha.core.settings import settings

translate_client = translate_v2.Client()

async def translate_text(
    text: str,
    source_language: str = "ne",
    target_language: str = "en",
) -> str:
    if settings.GEMINI_API_KEY:
        translated_text = translate_client.translate(
            text,
            target_language=target_language,
            source_language=source_language,
        )
        return translated_text["translatedText"]

    async with Translator() as translator:
        translated_text = ""
        for text_chunk in text.split("\n"):
            trans = await translator.translate(text_chunk, src=source_language, dest=target_language)
            translated_text += trans.text
        return translated_text


def translate_text_sync(
    text: str,
    source_language: str = "ne",
    target_language: str = "en",
) -> str:
    return asyncio.run(translate_text(text, source_language, target_language))

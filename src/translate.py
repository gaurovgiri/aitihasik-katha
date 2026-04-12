from googletrans import Translator
import  asyncio
from config import settings
from google.cloud import translate_v2

translate_client = translate_v2.Client()

async def translate_text(text, source_language="ne", target_language="en"):
    if settings.GEMINI_API_KEY:
        translated_text = translate_client.translate(text, target_language=target_language, source_language=source_language)
        return translated_text['translatedText']
        
    else:
        async with Translator() as translator:
            translated_text = ""
            for text_chunk in text.split("\n"):
                trans = await translator.translate(text_chunk, src=source_language, dest=target_language)
                translated_text += trans.text
            return translated_text



if __name__ == "__main__":
    text = "नेपाली भाषामा लेखिएको कुनै पाठ"
    translated_text = asyncio.run(translate_text(text))
    print(translated_text)
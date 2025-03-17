from googletrans import Translator
import  asyncio
import requests
from config import GCP_API_KEY

async def translate_text(text, source_language="ne", target_language="en"):
    if GCP_API_KEY:
        url = f"https://translation.googleapis.com/language/translate/v2?key={GCP_API_KEY}"
        data = {
            "q": text,
            "source": source_language,
            "target": target_language,
            "format": "text"
        }
        response = requests.post(url, data=data)
        return response.json()['data']['translations'][0]['translatedText']
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
from googletrans import Translator
import  asyncio

async def translate_text(text, source_language="ne", target_language="en"):
    async with Translator() as translator:
        translation = await translator.translate(text, src=source_language, dest=target_language)
        return translation.text

if __name__ == "__main__":
    # text = "नेपाली भाषामा लेखिएको कुनै पाठ"
    with open("src/test.txt", "r") as f:
        text = f.read()
    translated_text = asyncio.run(translate_text(text[:2000]))
    print(translated_text)
from vertexai.preview.vision_models import ImageGenerationModel
from PIL import Image
from config import settings
import os
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import time


generation_model = ImageGenerationModel.from_pretrained(settings.IMAGE_MODEL)
llm = ChatGoogleGenerativeAI(
    model=settings.IMAGE_CHAT_MODEL,
    api_key=settings.GEMINI_API_KEY
)


prompt_template = PromptTemplate.from_template("""
You are an expert prompt engineer for AI image generation.

Your task is to convert a historical narrative into a highly specific cinematic image prompt.

Full story (context only, do not summarize):
{full_story}

Current scene (focus here):
{current_scene}

Instructions:
- Focus ONLY on the current scene
- Extract key visual elements: characters, actions, setting, time period
- Be very specific about:
  - clothing
  - architecture
  - lighting
  - mood
  - camera framing (e.g., close-up, wide shot)
- Ensure historical accuracy
- Make each scene visually distinct
- Avoid generic descriptions
- No text or captions

Output format:
A single, highly detailed image generation prompt (no explanations).
""")

chain = prompt_template | llm | StrOutputParser()

def generate_image_prompt(current_scene, full_story):
    attempts = 0
    while attempts < 5:
        try:
            return chain.invoke({
                "full_story": full_story,
                "current_scene": current_scene
            })
        except Exception as e:
            print("LLM Error:", e)

            # crude quota detection (adjust if needed)
            if "quota" in str(e).lower() or "rate" in str(e).lower():
                print("Quota hit. Waiting 30 seconds...")
                time.sleep(30)
            else:
                time.sleep(5)

            attempts += 1

    raise Exception("Failed to generate prompt after retries")


def generate_image(current_scene, full_story, filename):
    prompt = generate_image_prompt(current_scene=current_scene, full_story=full_story)
    attempts_count = 0
    while attempts_count < 3:
        try:
            attempts_count += 1
            images = generation_model.generate_images(
                prompt=prompt,
                number_of_images=1,
                aspect_ratio="9:16",
                negative_prompt="",
                person_generation="",
                safety_filter_level="",
                add_watermark=True,
            )
            save_path = os.path.join(settings.IMAGE_PATH, filename)
            images[0].save(save_path)
            return filename

        except Exception as e:
            print("Error generating image:", e)
            print("Retrying...")
            time.sleep(30)
    
    if attempts_count == 3:
        print("Using fail safe image")
        fail_safe_image = Image.new("RGB", (768, 1408), color="black")
        save_path = os.path.join(settings.IMAGE_PATH, filename)
        fail_safe_image.save(save_path)
    
    return filename


if __name__ == "__main__":
    demo_prompt = "a painting of a beautiful sunset"
    generate_image(demo_prompt, "", "output.png")
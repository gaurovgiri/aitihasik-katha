import os
import time

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from PIL import Image
from vertexai.preview.vision_models import ImageGenerationModel

from ..core.settings import settings


generation_model = ImageGenerationModel.from_pretrained(settings.IMAGE_MODEL)
llm = ChatGoogleGenerativeAI(
    model=settings.IMAGE_CHAT_MODEL,
    api_key=settings.GEMINI_API_KEY,
)

prompt_template = PromptTemplate.from_template(
    """
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
"""
)

chain = prompt_template | llm | StrOutputParser()


def generate_image_prompt(current_scene: str, full_story: str) -> str:
    attempts = 0
    while attempts < 5:
        try:
            return chain.invoke(
                {
                    "full_story": full_story,
                    "current_scene": current_scene,
                }
            )
        except Exception as exc:
            print("LLM Error:", exc)
            if "quota" in str(exc).lower() or "rate" in str(exc).lower():
                print("Quota hit. Waiting 30 seconds...")
                time.sleep(30)
            else:
                time.sleep(5)
            attempts += 1

    raise RuntimeError("Failed to generate prompt after retries")


def generate_image(current_scene: str, full_story: str, filename: str) -> str:
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
                person_generation="allow_all",
                safety_filter_level=None,
                add_watermark=True,
            )
            save_path = os.path.join(settings.IMAGE_PATH, filename)
            images[0].save(save_path)
            return filename
        except Exception as exc:
            print("Error generating image:", exc)
            print("Retrying...")
            time.sleep(30)

    print("Using fail safe image")
    fail_safe_image = Image.new("RGB", (768, 1408), color="black")
    save_path = os.path.join(settings.IMAGE_PATH, filename)
    fail_safe_image.save(save_path)
    return filename

from vertexai.preview.vision_models import ImageGenerationModel
from PIL import Image
from config import settings
import os
from langchain_core.prompts import PromptTemplate
import time


generation_model = ImageGenerationModel.from_pretrained(settings.IMAGE_MODEL)

def build_prompt(current_scene, full_story):
    return PromptTemplate.from_template("""
        Create a cinematic, highly detailed image based on a historical narrative.

        Full story context (for consistency, do not illustrate entirely):
        {full_story}

        Current scene to depict (focus only on this moment):
        {current_scene}

        Instructions:
        - Focus only on the current scene while using the full story for context
        - Maintain consistency in characters, clothing, environment, and time period
        - Style: realistic, cinematic lighting, high detail, dramatic composition
        - Ensure historical accuracy (architecture, attire, setting)
        - Emotion and atmosphere should match the scene
        - No modern elements unless explicitly described
        - No text, captions, or watermarks in the image

        Output:
        A visually immersive 9:16 vertical composition with a clear subject and rich background.
    """).format(full_story=full_story, current_scene=current_scene)


def generate_image(current_scene, full_story, filename):
    prompt = build_prompt(current_scene=current_scene, full_story=full_story)
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
    prompt = "a painting of a beautiful sunset"
    generate_image(prompt, "", "output.png")
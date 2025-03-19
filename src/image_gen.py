from vertexai.preview.vision_models import ImageGenerationModel
from PIL import Image
from config import GCP_API_KEY, IMAGE_DIR, CHAT_MODEL
import os
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
import time


def generate_image(prompt, filename, model_name="imagen-3.0-generate-002"):
    generation_model = ImageGenerationModel.from_pretrained(model_name)
    llm = ChatOllama(model=CHAT_MODEL)
    template = """
    You are an AI assistant that will take sentences and refine the text to a prompt that is perfect to pass to a image generation model. The sentences are the segments of a historical story.
    Therefore the refined prompt should accurately descibe the image based on the sentences provided. Make sure that the refined prompt will not violate the safety guidelines of the image generation model.
    
    Sentences:
    {sentences}

    Refined Prompt:
    """

    prompt = ChatPromptTemplate.from_template(template).format(sentences=prompt)
    refined_prompt = llm.invoke(prompt).content.strip()
    attempts_count = 0
    while attempts_count < 3:
        try:
            attempts_count += 1
            images = generation_model.generate_images(
                prompt=refined_prompt,
                number_of_images=1,
                aspect_ratio="9:16",
                negative_prompt="",
                person_generation="",
                safety_filter_level="",
                add_watermark=True,
            )
            save_path = os.path.join(IMAGE_DIR, filename)
            images[0].save(save_path)
            break

        except Exception as e:
            print("Error generating image:", e)
            print("Retrying...")
            time.sleep(5)
    
    if attempts_count == 3:
        print("Using fail safe image")
        fail_safe_image = Image.new("RGB", (768, 1408), color="black")
        save_path = os.path.join(IMAGE_DIR, filename)
        fail_safe_image.save(save_path)

if __name__ == "__main__":
    prompt = "a painting of a beautiful sunset"
    generate_image(prompt, "output.png")
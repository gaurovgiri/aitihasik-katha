from vertexai.preview.vision_models import ImageGenerationModel
from PIL import Image
from config import GCP_API_KEY

def generate_image(prompt, model_name="imagen-3.0-generate-002"):
    generation_model = ImageGenerationModel.from_pretrained(model_name)
    images = generation_model.generate_images(
        prompt=prompt,
        number_of_images=1,
        aspect_ratio="1:1",
        negative_prompt="",
        person_generation="",
        safety_filter_level="",
        add_watermark=True,
    )
    return images[0].save("output.jpg")

if __name__ == "__main__":
    prompt = "a painting of a beautiful sunset"
    generate_image(prompt)
from config import settings
import pytesseract
import requests
import io
import base64

from google.cloud import vision

client = vision.ImageAnnotatorClient()

def extract_text(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    content = buffer.getvalue()
    image_obj = vision.Image(content=content)

    response = client.text_detection(image=image_obj)
    return response.full_text_annotation.text if response.full_text_annotation else ""
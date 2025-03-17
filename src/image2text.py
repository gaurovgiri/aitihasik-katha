from config import GCP_API_KEY, TESS_NEP_CONFIG
import pytesseract
import requests
import io
import base64
import json

def extract_text(image):
    if GCP_API_KEY:
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image = base64.b64encode(buffer.getvalue()).decode('utf-8')

        url = f'https://vision.googleapis.com/v1/images:annotate?key={GCP_API_KEY}'
        data = {
            "requests": [
                {
                    "image": {
                        "content": image
                    },
                    "features": [
                        {
                            "type": "TEXT_DETECTION"
                        }
                    ]
                }
            ]
        }
        response = requests.post(url, json=data)
        return response.json()['responses'][0]['fullTextAnnotation']['text']
    
    else:
        return pytesseract.image_to_string(image, config=TESS_NEP_CONFIG)

if __name__ == "__main__":
    from PIL import Image
    image = Image.open("data/images/3.png")
    text = extract_text(image)
    print(text)
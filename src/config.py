from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables
CHAT_MODEL = os.getenv("CHAT_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
GCP_API_KEY = os.getenv("GCP_API_KEY") 

# Pytesseract configuration
TESS_NEP_CONFIG = "--psm 6 --oem 3 -l nep"
TESS_ENG_NEP_CONFIG = "--psm 6 --oem 3 -l eng+nep"

# Data Directories
DATA_DIR = "data"
AUDIO_DIR = f"{DATA_DIR}/audio"
IMAGE_DIR = f"{DATA_DIR}/images"
VIDEO_DIR = f"{DATA_DIR}/videos"
PDF_DIR = f"{DATA_DIR}/pdfs"
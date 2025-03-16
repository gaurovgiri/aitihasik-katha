from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables
CHAT_MODEL=os.getenv("CHAT_MODEL")
EMBEDDING_MODEL=os.getenv("EMBEDDING_MODEL")
COLLECTION_NAME=os.getenv("COLLECTION_NAME")



# Pytesseract configuration
TESS_NEP_CONFIG = "--psm 6 --oem 3 -l nep"
TESS_ENG_NEP_CONFIG = "--psm 6 --oem 3 -l eng+nep"
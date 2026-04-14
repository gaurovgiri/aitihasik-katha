from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

    GEMINI_API_KEY: str = ""
    EMBEDDING_MODEL: str = ""
    CHAT_MODEL: str = ""
    IMAGE_CHAT_MODEL: str = ""
    IMAGE_MODEL: str = ""
    AUDIO_MODEL: str = ""

    PROJECT_ID: str = ""
    LOCATION: str = ""
    BUCKET: str = ""
    BUCKET_URI: str = ""

    GOOGLE_APPLICATION_CREDENTIALS: str = ""

    DISPLAY_NAME: str = ""
    INDEX_ID: str = ""
    INDEX_ENDPOINT_ID: str = ""
    DEPLOYED_INDEX_ID: str = ""

    TESS_NEP_CONFIG: str = "--psm 6 --oem 3 -l nep"
    TESS_ENG_NEP_CONFIG: str = "--psm 6 --oem 3 -l eng+nep"

    IMAGE_PATH: str = "data/images/"
    VIDEO_PATH: str = "data/videos/"
    AUDIO_PATH: str = "data/audios/"
    OUTPUT_PATH: str = "data/output/"


load_dotenv()
settings = Settings()


def ensure_directories() -> None:
    """Create output directories expected by the pipeline."""
    for value in [
        settings.IMAGE_PATH,
        settings.VIDEO_PATH,
        settings.AUDIO_PATH,
        settings.OUTPUT_PATH,
    ]:
        Path(value).mkdir(parents=True, exist_ok=True)

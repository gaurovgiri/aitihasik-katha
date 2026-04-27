import requests
from aitihasik_katha.core.settings import settings
from aitihasik_katha.core.logging import get_logger
import time


logger = get_logger(__name__)

class InstagramService:
    BASE_URL = "https://graph.facebook.com/v25.0"

    def __init__(self, client_id, client_secret, short_lived_token=None, user_id=None, page_access_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.short_lived_token = short_lived_token
        self.user_id = user_id
        self.page_access_token = page_access_token

    
    def _get(self, url: str, params: dict) -> dict:
        """Helper: GET request with error handling."""
        response = requests.get(url, params=params, timeout=30)
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            try:
                details = response.json()
            except ValueError:
                details = {"raw": response.text}
            raise RuntimeError(f"Request failed: {details}") from exc
        logger.debug("Instagram GET %s returned status %s", url, response.status_code)
        return response.json()
    
    def _post(self, url: str, params: dict) -> dict:
        """Helper: GET request with error handling."""
        response = requests.post(url, params=params, timeout=30)
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            try:
                details = response.json()
            except ValueError:
                details = {"raw": response.text}
            raise RuntimeError(f"Request failed: {details}") from exc
        return response.json()
    
    def get_user_id(self):
        url = f"{self.BASE_URL}/me"
        params = {
            "fields": "instagram_business_account"
        }
        data = self._get(url, params)
        return data["instagram_business_account"]["id"]

    def get_long_lived_token(self):
        url = f"{self.BASE_URL}/oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "fb_exchange_token": self.short_lived_token
        }
        data = self._get(url, params)
        return data["access_token"]
    
    def get_page_access_token(self, long_lived_token: str) -> tuple[str, str]:
        """Step 2: Get the never-expiring Page Access Token."""
        url = f"{self.BASE_URL}/me/accounts"
        params = {
            "access_token": long_lived_token
        }
        data = self._get(url, params)
        pages = data.get("data", [])
        if not pages:
            raise RuntimeError("No pages found. Make sure your app is linked to a Facebook Page.")

        page = pages[0]

        return page["access_token"]
    
    def create_media_container(self, media_url, caption, media_type="REELS"):
        url = f"{self.BASE_URL}/{self.user_id}/media"
        media_type = media_type.strip().upper()
        media_configs = {
            "IMAGE": {
                "image_url": media_url,
                "caption": caption,
            },
            "REELS": {
                "media_type": "REELS",
                "video_url": media_url,
                "caption": caption,
                "thumb_offset": 0,
            }
        }

        if media_type not in media_configs:
            raise ValueError(f"Unsupported media_type: {media_type}")

        params = {
            **media_configs[media_type],
            "access_token": self.page_access_token
        }
        try:
            response = self._post(url, params)
            media_id = response.get("id")
            return media_id
        except RuntimeError as exc:
            logger.error("Failed creating media container: %s", exc)
            return ""


    def upload_media(self, media_url, caption, media_type="REELS"):
        media_container_id = self.create_media_container(
            media_url, caption, media_type
        )

        if media_container_id:
            publish_url = f"{self.BASE_URL}/{self.user_id}/media_publish"
            params = {
                "creation_id": media_container_id,
                "access_token": self.page_access_token,
            }

            while not self.is_media_ready(media_container_id):
                logger.info("Media not ready, retrying after 1 minute")
                time.sleep(60)
            try:
                response = self._post(publish_url, params)
                if response:
                    logger.info(
                        "Post published for caption preview: %s...",
                        caption if len(caption) < 50 else caption[:50],
                    )
            except RuntimeError as exc:
                logger.error("Error uploading to Instagram: %s", exc)
        else:
            logger.error("Failed to create media container")
    
    def is_media_ready(self, media_container_id: str) -> bool:
        """Check Instagram media container processing status."""
        url = f"{self.BASE_URL}/{media_container_id}"
        params = {
            "access_token": self.page_access_token,
            "fields": "status_code",
        }
        data = self._get(url, params)
        if data.get("status_code") == "ERROR":
            raise RuntimeError("Media upload failed!")
        return data.get("status_code") == "FINISHED"


instagram = InstagramService(
        settings.INSTAGRAM_CLIENT_ID, settings.INSTAGRAM_CLIENT_SECRET,
        page_access_token=settings.INSTAGRAM_PAGE_ACCESS_TOKEN, user_id=settings.INSTAGRAM_USER_ID
    )

if __name__ == "__main__":
    with open("runs/82b7f3cb-c7c1-48b3-b072-c378b4bc05c6/output/caption.txt", "r", encoding="utf-8") as cap_file:
        caption_text = cap_file.read()
    instagram.upload_media(
        "https://storage.googleapis.com/aitihasik-katha-bucket/runs/82b7f3cb-c7c1-48b3-b072-c378b4bc05c6/output/final_video.mp4",
        caption_text,
        "REELS"
    )
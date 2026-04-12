import os
from google.cloud import storage
import os

def upload_file_to_gcs(bucket_name: str, source_file_path: str, destination_blob_path: str) -> str:
    """
    Uploads a file to Google Cloud Storage and returns the GCS path.

    Args:
        bucket_name (str): GCS bucket name
        source_file_path (str): Local file path
        destination_blob_path (str): Path inside bucket (e.g. folder/file.mp3)

    Returns:
        str: gs://bucket_name/destination_blob_path
    """

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    blob = bucket.blob(destination_blob_path)
    blob.upload_from_filename(source_file_path)

    gcs_path = f"gs://{bucket_name}/{destination_blob_path}"
    return gcs_path

def delete_file_from_gcs(gcs_path: str) -> bool:
    """
    Deletes a file from Google Cloud Storage given its gs:// path.

    Args:
        gcs_path (str): Full GCS path (gs://bucket_name/blob_path)

    Returns:
        bool: True if deleted successfully, False otherwise
    """

    if not gcs_path.startswith("gs://"):
        raise ValueError("Invalid GCS path. Must start with gs://")

    path_parts = gcs_path.replace("gs://", "").split("/", 1)
    bucket_name = path_parts[0]
    blob_path = path_parts[1]

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    if blob.exists():
        blob.delete()
        return True

    return False



def clear():
    audio_files = os.listdir("data/audio")
    image_files = os.listdir("data/images")
    video_files = os.listdir("data/videos")
    output_files = os.listdir("data/output")
    for file in audio_files:
        os.remove(f"data/audio/{file}")
    for file in image_files:
        os.remove(f"data/images/{file}")
    for file in video_files:
        os.remove(f"data/videos/{file}")
    for file in output_files:
        os.remove(f"data/output/{file}")
    print("Cleared all files")


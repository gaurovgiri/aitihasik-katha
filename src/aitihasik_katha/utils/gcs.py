from google.cloud import storage


def upload_file_to_gcs(bucket_name: str, source_file_path: str, destination_blob_path: str, return_public: bool = True) -> str:
    """Upload a local file to GCS and return its gs:// URI."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_path)
    blob.upload_from_filename(source_file_path)
    if return_public:
        return f"https://storage.googleapis.com/{bucket_name}/{destination_blob_path}"
    return f"gs://{bucket_name}/{destination_blob_path}"


def delete_file_from_gcs(gcs_path: str) -> bool:
    """Delete an object in GCS from its gs:// URI."""
    if not gcs_path.startswith("gs://"):
        raise ValueError("Invalid GCS path. Must start with gs://")

    bucket_name, blob_path = gcs_path.replace("gs://", "", 1).split("/", 1)
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    if blob.exists():
        blob.delete()
        return True
    return False

from google.cloud import storage
import uuid
from fastapi import UploadFile

GCS_BUCKET_NAME = "object-identity-images-neat-planet-483104-t8"

async def upload_file_to_gcs(file: UploadFile) -> str:
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)

    # Generate a unique filename in the /raw folder
    blob_name = f"raw/{uuid.uuid4()}_{file.filename}"
    blob = bucket.blob(blob_name)

    # Upload contents
    contents = await file.read()  # read file into memory
    blob.upload_from_string(contents, content_type=file.content_type)

    # Return GCS URI
    return f"gs://{GCS_BUCKET_NAME}/{blob_name}"
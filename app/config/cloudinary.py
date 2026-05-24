import os
import cloudinary
import cloudinary.uploader
from cloudinary.uploader import upload
from fastapi import HTTPException, status, UploadFile
from typing import List

CLOUDINARY_CLOUD_NAME=os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY=os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET=os.getenv("CLOUDINARY_API_SECRET")

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

async def upload_image(image: UploadFile):
    try:
        upload_result = upload(image.file)
        file_url = upload_result['secure_url']
        return file_url
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error uploading images: {e}")

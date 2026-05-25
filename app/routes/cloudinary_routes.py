from cloudinary.uploader import upload
from app.config.cloudinary import cloudinary
from app.middleware.auth import User, get_current_user
from fastapi import APIRouter, HTTPException, status, UploadFile, Depends
from typing import List
from app.config.cloudinary import upload_image
from app.middleware.auth import authMiddleware
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/cloudinary", tags=["Cloudinary"])

@router.post("/upload")
async def image_upload(image: UploadFile, current_user: User = Depends(authMiddleware), db: Session = Depends(get_db)):
    try:
        url = await upload_image(image)
        return {
            "data": {
                "url": url
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
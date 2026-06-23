from fastapi import APIRouter, UploadFile, File
import shutil
import os

router = APIRouter(
    prefix="/api/upload",
    tags=["Upload"]
)

@router.post("/")
def upload_image(
    file: UploadFile = File(...)
):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "image_url": f"/uploads/{file.filename}"
    }
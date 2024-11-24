from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app import models, schemas, database
import shutil
import os

router = APIRouter()


@router.post("/upload", response_model=schemas.Photo)
def upload_photo(description: str, file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    file_location = f"static/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_photo = models.Photo(description=description, filename=file.filename)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

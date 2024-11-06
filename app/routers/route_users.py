from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ..crud import crud_users
from .. import models, schemas
from ..database import SessionLocal, engine
from typing import List
import pandas as pd
from io import BytesIO


models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload_excel/")
async def upload_users_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not (file.filename.endswith(".xlsx") or file.filename.endswith(".xls")):
        raise HTTPException(status_code=400, detail="File must be an Excel file")

    file_content = await file.read()
    
    try:
        df = pd.read_excel(BytesIO(file_content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar el archivo Excel: {e}")

    required_columns = {'fullname', 'email'}
    if not required_columns.issubset(df.columns):
        raise HTTPException(status_code=400, detail="El archivo Excel debe contener las columnas 'fullname' y 'email'")

    users_data = df.to_dict(orient="records")

    result = crud_users.create_user_bulk(db, users_data)
    return {"message": "Users created successfully", "result": result}

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return crud_users.create_user(db=db, user=user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user. {e}")

@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = crud_users.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="user not found")
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user. {e}")

@router.get("/", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        return crud_users.get_users(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get users. {e}")
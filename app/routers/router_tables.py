from fastapi import APIRouter, Depends, HTTPException, UploadFile,File
from sqlalchemy.orm import Session
from ..crud import crud_tables
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
        
@router.post("/", response_model=schemas.Table)
def create_table(table:schemas.TableCreate, db:Session = Depends(get_db)):
    try:
        return crud_tables.create_table(db=db, table=table)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid table data: {e}")
    
@router.post("/upload_excel_tables")
async def upload_tables_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not (file.filename.endswith("xlsx") or file.filename.endswith("xls")):
        raise HTTPException(status_code=400, detail="File must be an Excel File")
    
    file_content = await file.read()
    
    try:
        df = pd.read_excel(BytesIO(file_content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Excel file: {e}")
    
    required_columns = {"table_number","capacity"}
    if not required_columns.issubset(df.columns):
        raise HTTPException(status_code=400, detail="Invalid Excel file. missing required columns: 'table_name' and 'capacity'")
    
    tables_data = df.to_dict(orient="records")
    result = crud_tables.create_table_bulk(db, tables_data)
    return {"message": "Tables created successfully", "result": result}

@router.delete("/delete_table/{table_id}", response_model=dict)
def delete_table_endpoint(table_id: int, db: Session = Depends(get_db)):
    return crud_tables.delete_table(db=db, table_id=table_id)

@router.put("/update_table/{table_id}", response_model=schemas.Table)
def update_table(table_id: int, table_data: schemas.TableUpdate, db: Session = Depends(get_db)):
    try:
        return crud_tables.update_table(db=db, table_id=table_id, table_data=table_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid table data: {e}")
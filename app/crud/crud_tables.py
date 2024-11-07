from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException   

def create_table(db:Session, table: schemas.TableCreate):
    try:
        db_table = models.RestaurantTable(table_number=table.table_number, capacity=table.capacity)
        db.add(db_table)
        db.commit()
        db.refresh(db_table)
        return db_table
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error Trying Table Create: {e}")
    
def create_table_bulk(db:Session, tables_data: list):
    try:
        for table_data in tables_data:
            table = models.RestaurantTable(**table_data)
            db.add(table)
        db.commit()
        return {"total_tables": len(tables_data), "status": "completed"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error While Trie Create Bulk Of Tables: {e}")
            
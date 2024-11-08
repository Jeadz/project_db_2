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
            
def delete_table(db:Session, table_id: int):
    try:
        table = db.query(models.RestaurantTable).filter(models.RestaurantTable.id == table_id).first()
        
        if not table:
            raise HTTPException(status_code=404, detail="Table Not Found")
        db.delete(table)
        db.commit()
        return {"message":"Table Delete Successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Error Trying Delete Table: {e}')
    
def update_table(db:Session, table_id:int, table_data: schemas.TableUpdate):
    try:
        db_table = db.query(models.RestaurantTable).filter(models.RestaurantTable.id == table_id).first()
        
        if not db_table:
            raise HTTPException(status_code=404, detail="Table Not Found")
        
        if table_data.table_number is not None:
            db_table.table_number = table_data.table_number
        if table_data.capacity is not None:
            db_table.capacity = table_data.capacity
           
        db.commit()
        db.refresh(db_table)
        return db_table
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error Trying Table Update: {e}")
    
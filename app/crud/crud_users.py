from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException   


def create_user_bulk(db: Session, users_data: list):
    for user_data in users_data:
        user = models.User(**user_data)
        db.add(user)
    db.commit()
    return {"total_users": len(users_data), "status": "completed"}

def delete_user(db:Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    db.delete(user)
    db.commit()
    return {"message": "User Delete Successfully"}
    
def get_user(db: Session, user_id: int):
    try:
        return db.query(models.User).filter(models.User.id == user_id).first()
    except Exception as e:
        print(f"Error: {e}")

def create_user(db: Session, user: schemas.UserCreate):
    try:
        db_user = models.User(fullname=user.fullname, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(f"Error: {e}")
        
def get_users(db: Session):
    return db.query(models.User).all()



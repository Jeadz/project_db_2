from sqlalchemy.orm import Session
from .. import models, schemas


def create_user_bulk(db: Session, users_data: list):
    for user_data in users_data:
        user = models.User(**user_data)
        db.add(user)
    db.commit()
    return {"total_users": len(users_data), "status": "completed"}

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



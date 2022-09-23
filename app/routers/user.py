from fastapi import HTTPException, Depends, APIRouter
from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post("/users", status_code=201, response_model = schemas.UserCreateResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash_password(user.password)
    
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/users", response_model=List[schemas.UserCreateResponse])
def get_all_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users

@router.get("/users/{id}", response_model=schemas.UserCreateResponse)
def get_single_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="The requested resource could not be found")
    return user

@router.put("users/{id}", response_model=schemas.UserCreateResponse)
def update_user(id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=404, detail="The requested resource could not be found")

    user_query.update(updated_user.dict(), synchronize_session = False)
    db.commit()

    return user_query.first()    

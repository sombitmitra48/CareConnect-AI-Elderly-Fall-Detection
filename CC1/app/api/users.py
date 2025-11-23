from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(models.user.User).filter(models.user.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    # Create new user
    db_user = models.user.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        phone_number=user.phone_number,
        role=user.role,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user fields
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    
    return None

@router.post("/{user_id}/locations/", response_model=schemas.Location)
def create_user_location(user_id: int, location: schemas.LocationCreate, db: Session = Depends(get_db)):
    # Verify user exists
    db_user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create location
    db_location = models.user.Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    
    return db_location
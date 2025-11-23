from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Alert)
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    # Verify user exists
    db_user = db.query(models.user.User).filter(models.user.User.id == alert.user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create alert
    db_alert = models.user.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    
    return db_alert

@router.get("/{alert_id}", response_model=schemas.Alert)
def read_alert(alert_id: int, db: Session = Depends(get_db)):
    db_alert = db.query(models.user.Alert).filter(models.user.Alert.id == alert_id).first()
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return db_alert

@router.get("/", response_model=List[schemas.Alert])
def read_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alerts = db.query(models.user.Alert).offset(skip).limit(limit).all()
    return alerts

@router.put("/{alert_id}", response_model=schemas.Alert)
def update_alert(alert_id: int, alert: schemas.AlertUpdate, db: Session = Depends(get_db)):
    db_alert = db.query(models.user.Alert).filter(models.user.Alert.id == alert_id).first()
    if db_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    # Update alert fields
    for key, value in alert.dict().items():
        setattr(db_alert, key, value)
    
    db.commit()
    db.refresh(db_alert)
    
    return db_alert
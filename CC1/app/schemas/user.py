from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ELDERLY = "elderly"
    CAREGIVER = "caregiver"
    VOLUNTEER = "volunteer"
    DOCTOR = "doctor"
    ADMIN = "admin"

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    phone_number: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class LocationBase(BaseModel):
    latitude: str
    longitude: str
    address: str
    is_primary: bool = False

class LocationCreate(LocationBase):
    user_id: int

class LocationUpdate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class AlertBase(BaseModel):
    location_lat: str
    location_lng: str
    status: str
    alert_type: str
    notes: Optional[str] = None

class AlertCreate(AlertBase):
    user_id: int

class AlertUpdate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    user_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True
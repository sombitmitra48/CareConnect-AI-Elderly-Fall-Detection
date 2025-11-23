from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as PyEnum

class UserRole(str, PyEnum):
    ELDERLY = "elderly"
    CAREGIVER = "caregiver"
    VOLUNTEER = "volunteer"
    DOCTOR = "doctor"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    phone_number = Column(String)
    role = Column(Enum(UserRole))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    locations = relationship("Location", back_populates="user")
    alerts = relationship("Alert", back_populates="user")

class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    latitude = Column(String)
    longitude = Column(String)
    address = Column(String)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="locations")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    location_lat = Column(String)
    location_lng = Column(String)
    status = Column(String)  # pending, acknowledged, resolved
    alert_type = Column(String)  # fall_detected, manual_trigger, etc.
    notes = Column(String)
    
    # Relationships
    user = relationship("User", back_populates="alerts")
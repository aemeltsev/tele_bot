import os

from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, JSON, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DB_URL')

# Create a connection to the database
engine = create_engine(db_url)

# Creating a session factory to work with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# The User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    ities = relationship("City", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(user_id={self.user_id}, created_at={self.created_at}, is_active={self.is_active})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "token": self.token,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
            }

# The City model
class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    user = relationship("User", back_populates="cities")
    forecast = relationship("Forecast", back_populates="city", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_city_name', 'name'),
        Index('idx_city_coordinates', 'latitude', 'longitude')
    )

    def __repr__(self):
        return f"City(name={self.name}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            }

# The Forecast model
class Forecast(Base):
    __tablename__ = "weather_forecasts"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey('cities.id', ondelete='CASCADE'), nullable=False, index=True)
    forecast_data = Column(JSON)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(datetime.timezone.utc))
    
    city = relationship("City", back_populates="forecast")

    def __repr__(self):
        return f"Forecast(id={self.id}, city_id={self.city_id})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "city_id": self.city_id,
            "forecast_data": self.forecast_data,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
            }


# Creating tables in the database
Base.metadata.create_all(bind=engine)
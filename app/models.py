from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String, index=True, nullable=False)
    machine_name = Column(String, nullable=False)
    temperature_c = Column(Float, nullable=False)
    vibration_hz = Column(Float, nullable=False)
    status = Column(String, default="unknown")
    recorded_at = Column(DateTime, server_default=func.now())

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MachineCreate(BaseModel):
    name: str
    location: str


class MachineResponse(BaseModel):
    id: int
    name: str
    location: str
    created_at: datetime

    class Config:
        from_attributes = True  # allows Pydantic to read SQLAlchemy objects


class SensorReadingCreate(BaseModel):
    sensor_id: str
    machine_name: str
    temperature_c: float = Field(..., ge=-273.15, description="Celsius temperature")
    vibration_hz: float = Field(..., ge=0, description="Must be non-negative")
    status: Optional[str] = "unknown"  # has a default, so not required


# If you ever change a field in SensorReadingCreate, SensorReadingResponse updates automatically.
class SensorReadingResponse(SensorReadingCreate):  # inherits all fields above
    id: int
    recorded_at: datetime

    class Config:
        from_attributes = True  # allows Pydantic to read SQLAlchemy objects

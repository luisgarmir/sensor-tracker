from platform import machine
from pyexpat import model
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, get_db, Base
from app import models, schemas

# Creates all tables in the database on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sensor Tracker", description="Sensor API")


# --- MACHINE ROUTES ---


@app.post("/machines", response_model=schemas.MachineResponse, status_code=201)
def create_machine(machine: schemas.MachineCreate, db: Session = Depends(get_db)):
    # Check if machine already exists
    existing = (
        db.query(models.Machine).filter(models.Machine.name == machine.name).first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Machine already exists")

    new_machine = models.Machine(name=machine.name, location=machine.location)
    db.add(new_machine)
    db.commit()
    db.refresh(new_machine)  # loads the new id and created_at from db
    return new_machine


@app.get("/machines", response_model=list[schemas.MachineResponse])
def get_machines(db: Session = Depends(get_db)):
    return db.query(models.Machine).all()


# --- SENSOR READINGS ROUTES ---


@app.post(
    "/sensors/readings", response_model=schemas.SensorReadingResponse, status_code=201
)
def create_sensor_reading(
    sensor_reading: schemas.SensorReadingCreate, db: Session = Depends(get_db)
):

    new_sensor_reading = models.SensorReading(
        sensor_id=sensor_reading.sensor_id,
        machine_name=sensor_reading.machine_name,
        temperature_c=sensor_reading.temperature_c,
        vibration_hz=sensor_reading.vibration_hz,
    )
    db.add(new_sensor_reading)
    db.commit()
    db.refresh(new_sensor_reading)
    return new_sensor_reading


@app.get("/sensors/readings", response_model=list[schemas.SensorReadingResponse])
def get_sensor_readings(db: Session = Depends(get_db)):
    return db.query(models.SensorReading).all()

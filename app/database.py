from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# The connection string — sqlite creates a local file called sensor_tracker.db
DATABASE_URL = "sqlite:///./sensor_tracker.db"

# The engine — knows WHERE the database is
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # needed only for SQLite
)

# The session factory — every session we open will use this engine
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# Base class — all our models will inherit from this
class Base(DeclarativeBase):
    pass


# Dependency — FastAPI will call this before every route that needs the DB
def get_db():
    db = SessionLocal()  # open a session
    try:
        yield db  # hand it to the route
    finally:
        db.close()  # always close it, even if an error happened

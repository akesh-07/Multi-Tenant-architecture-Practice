from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

# Initialize the database engine with the connection URL
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    # Provide a transactional scope around a series of operations
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

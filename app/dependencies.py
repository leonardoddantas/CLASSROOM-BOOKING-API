from app.database import SessionLocal
from sqlalchemy.orm import Session

def get_session():
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
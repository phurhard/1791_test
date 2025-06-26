from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from api.core.settings import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)
Base = declarative_base()

def init_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

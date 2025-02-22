from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import configsetting

# Create the database engine using the configured database URL
engine = create_engine(configsetting.DATABASE_URL)

# Create a session factory with autocommit and autoflush disabled
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


class Wishes(Base):
    """
    Represents the 'wishes' table in the database.

    Attributes:
        id (int): The primary key, auto-incrementing identifier.
        datetime (datetime): Timestamp of when the wish was created.
        username (str): The name of the user making the wish.
        wish (str): The wish content.
    """

    __tablename__ = "wishes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    username = Column(String(50), nullable=False)
    wish = Column(Text, nullable=False)


# Create the 'wishes' table in the database if it doesn't exist
Base.metadata.create_all(bind=engine)


def get_db():
    """
    Provides a database session for dependency injection.

    Yields:
        Session: A new database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

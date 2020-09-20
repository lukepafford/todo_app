from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from todo_app.config import DB_URL
from datetime import datetime

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column("description", String, nullable=True)
    completed = Column("completed", Boolean, default=False)
    created_at = Column("created_at", DateTime, default=datetime.now)
    updated_at = Column("updated_at", DateTime, default=datetime.now)


def get_session():
    return SessionLocal()

from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True


class Todo(OrmBaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

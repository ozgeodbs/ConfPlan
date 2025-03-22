from sqlalchemy import Column, Integer

from models.base import BaseModel
from models.db import db

class Hall(BaseModel):
    __tablename__ = 'Hall'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Capacity = Column(Integer, nullable=False)
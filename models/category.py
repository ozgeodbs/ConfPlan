from sqlalchemy import Column, Integer, String, DateTime
from models.db import db
from models.base import BaseModel

class Category(BaseModel):
    __tablename__ = 'Category'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String(100), nullable=False)  # Title cannot be null
from sqlalchemy import Column, Integer, String, DateTime
from models.db import db
from models.base import BaseModel

class Category(BaseModel):
    __tablename__ = 'Category'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String(100), nullable=False)  # Title cannot be null
    CreatedDate = Column(DateTime, default=db.func.current_timestamp())  # Default to current timestamp
    ChangedDate = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # Update on change

    # You can remove the __repr__ method if you don't need it

from sqlalchemy import Column, Integer, String, SmallInteger, Boolean, DateTime
from models.base import BaseModel

class Category(BaseModel):
    __tablename__ = 'category'

    Id = Column(SmallInteger, primary_key=True)
    Title = Column(String(100))

    def __repr__(self):
        return f"<Category(id={self.Id}, title={self.Title})>"

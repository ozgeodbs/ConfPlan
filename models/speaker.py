from sqlalchemy import Column, Integer, String
from models.base import BaseModel

class Speaker(BaseModel):
    __tablename__ = 'Speaker'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(100), nullable=False)
    LastName = Column(String(100), nullable=False)
    Bio = Column(String(255))
    Email = Column(String(100), nullable=False, unique=True)
    Phone = Column(String(20))
    PhotoUrl = Column(String(255))

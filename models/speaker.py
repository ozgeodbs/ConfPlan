from sqlalchemy import Column, Integer, String
from models.base import BaseModel
from models.db import db

class Speaker(BaseModel):
    __tablename__ = 'Speaker'

    Id = Column(Integer, primary_key=True, autoincrement=True)  # Primary Key
    FirstName = Column(String(100), nullable=False)  # Speaker's first name
    LastName = Column(String(100), nullable=False)  # Speaker's last name
    Bio = Column(String(255))  # Speaker's bio (can be optional)
    Email = Column(String(100), nullable=False, unique=True)  # Speaker's email (unique)
    Phone = Column(String(20))  # Speaker's phone (optional)
    PhotoUrl = Column(String(255))

    def to_dict(self):
        return {
            "Id": self.Id,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "Email": self.Email,
            "Phone": self.Phone,
            "PhotoUrl": self.PhotoUrl
        }
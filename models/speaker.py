from sqlalchemy import Column, Integer, String
from models.db import db

class Speaker(db.Model):
    __tablename__ = 'Speaker'

    Id = Column(Integer, primary_key=True)
    FirstName = Column(String(100), nullable=False)
    LastName = Column(String(100), nullable=False)
    Bio = Column(String(255))

    def __repr__(self):
        return f"<Speaker(id={self.Id}, name={self.FirstName} {self.LastName})>"

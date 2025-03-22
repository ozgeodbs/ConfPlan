from sqlalchemy import Column, Integer
from models.db import db

class Hall(db.Model):
    __tablename__ = 'Hall'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Capacity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Hall(id={self.Id}, capacity={self.Capacity})>"

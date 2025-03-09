from sqlalchemy import Column, Integer, SmallInteger, Boolean, DateTime
from models.base import BaseModel


class Hall(BaseModel):
    __tablename__ = 'hall'

    Id = Column(Integer, primary_key=True)
    Capacity = Column(SmallInteger)  # Salonun kapasitesi

    def __repr__(self):
        return f"<Hall(id={self.Id}, capacity={self.Capacity})>"

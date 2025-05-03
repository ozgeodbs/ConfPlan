from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import BaseModel
from models.db import db

class Hall(BaseModel):
    __tablename__ = 'Hall'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Capacity = Column(Integer, nullable=False)
    ConferenceId = Column(Integer, ForeignKey('Conference.Id'), nullable=False)
    Title = Column(String(255), nullable=False)

    conference = db.relationship('Conference', backref='halls')
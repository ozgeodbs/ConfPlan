from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from models.base import BaseModel
from models.db import db

class Paper(BaseModel):
    __tablename__ = 'Paper'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String(255), nullable=False)
    ConferenceId = Column(Integer, ForeignKey('Conference.Id'), nullable=False)
    SpeakerId = Column(Integer, ForeignKey('Speaker.Id'), nullable=False)
    CategoryId = Column(Integer, ForeignKey('Category.Id'), nullable=False)
    Duration = Column(Integer)
    Description = Column(Text)
    HallId = Column(Integer, ForeignKey('Hall.Id'), nullable=False)
    StartTime = Column(DateTime, nullable=True)
    EndTime = Column(DateTime, nullable=True)

    conference = db.relationship('Conference', backref='papers')
    category = db.relationship('Category', backref='papers')
    speaker = db.relationship('Speaker', backref='papers')
    hall = db.relationship('Hall', backref='papers')
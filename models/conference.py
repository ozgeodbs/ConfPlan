from sqlalchemy import Column, Integer, String, DateTime

from models.base import BaseModel

class Conference(BaseModel):
    __tablename__ = 'Conference'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String(200), nullable=False)
    StartDate = Column(DateTime, nullable=False)
    EndDate = Column(DateTime, nullable=False)
    Location = Column(String(200), nullable=False)
    Organizer = Column(String(100), nullable=False)
    PhotoUrl = Column(String(300), nullable=False)
    VideoUrl = Column(String(300), nullable=False)

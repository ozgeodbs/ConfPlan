from sqlalchemy import Column, Integer, String, Date

from models.base import BaseModel

class Conference(BaseModel):
    __tablename__ = 'Conference'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String(200), nullable=False)
    StartDate = Column(Date, nullable=False)
    EndDate = Column(Date, nullable=False)
    Location = Column(String(200), nullable=False)
    Organizer = Column(String(100), nullable=False)
    PhotoUrl = Column(String(300), nullable=False)
    VideoUrl = Column(String(300), nullable=False)

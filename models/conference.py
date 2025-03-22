from sqlalchemy import Column, Integer, String, Date
from models.db import db

class Conference(db.Model):
    __tablename__ = 'Conference'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String(200), nullable=False)
    StartDate = Column(Date, nullable=False)
    EndDate = Column(Date, nullable=False)
    Location = Column(String(200), nullable=False)
    Organizer = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Conference(id={self.Id}, title={self.Title})>"

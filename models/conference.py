from sqlalchemy import Column, Integer, String, DateTime
from models.base import BaseModel

class Conference(BaseModel):
    __tablename__ = 'conference'

    Id = Column(Integer, primary_key=True)
    Title = Column(String(150))
    StartDate = Column(DateTime)
    EndDate = Column(DateTime)
    Location = Column(String(250))
    Organizer = Column(String(500))

    def __repr__(self):
        return f"<Conference(id={self.Id}, title={self.Title})>"

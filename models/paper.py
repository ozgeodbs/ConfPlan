from sqlalchemy import Column, Integer, String, SmallInteger, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel

class Paper(BaseModel):
    __tablename__ = 'paper'

    Id = Column(Integer, primary_key=True)
    Title = Column(String(150))
    SpeakerId = Column(Integer, ForeignKey('speaker.Id'))
    CategoryId = Column(SmallInteger, ForeignKey('category.Id'))
    Duration = Column(Integer)
    Description = Column(String(500))
    HallId = Column(SmallInteger, ForeignKey('hall.Id'))

    speaker = relationship("Speaker")
    category = relationship("Category")
    hall = relationship("Hall")

    def __repr__(self):
        return f"<Paper(id={self.Id}, title={self.Title}, speaker={self.speaker.FirstName} {self.speaker.LastName})>"

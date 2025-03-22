from sqlalchemy import Column, Integer, String, Text, ForeignKey
from models.db import db
from models.category import Category  # Category modelini içe aktar

class Paper(db.Model):
    __tablename__ = 'Paper'  # Tablo adı büyük harflerle

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String(255), nullable=False)
    SpeakerId = Column(Integer, ForeignKey('Speaker.Id'), nullable=False)  # SpeakerId ile ilişki
    CategoryId = Column(Integer, ForeignKey('Category.Id'), nullable=False)  # CategoryId ile ilişki
    Duration = Column(Integer)
    Description = Column(Text)
    HallId = Column(Integer, ForeignKey('Hall.Id'), nullable=False)  # HallId ile ilişki

    category = db.relationship('Category', backref='papers')  # Category ile ilişki
    speaker = db.relationship('Speaker', backref='papers')  # Speaker ile ilişki
    hall = db.relationship('Hall', backref='papers')  # Hall ile ilişki

    def __repr__(self):
        return f"<Paper(id={self.Id}, title={self.Title})>"

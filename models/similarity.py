from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import BaseModel
from models.db import db


class Similarity(BaseModel):
    __tablename__ = 'Similarity'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    PaperId = Column(Integer, ForeignKey('Paper.Id'), nullable=False)
    SimilarPaperId = Column(Integer, ForeignKey('Paper.Id'), nullable=False)
    SimilarityScore = Column(Float, nullable=False)
    PaperTitle = Column(String(255), nullable=False)  # Paper başlığı
    SimilarPaperTitle = Column(String(255), nullable=False)  # Similar Paper başlığı

    paper = db.relationship('Paper', foreign_keys=[PaperId], backref='similarities')
    similar_paper = db.relationship('Paper', foreign_keys=[SimilarPaperId], backref='similar_to')

    __table_args__ = (
        db.UniqueConstraint('PaperId', 'SimilarPaperId', name='_paper_similarity_uc'),
    )

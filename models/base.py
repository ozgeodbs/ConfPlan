from sqlalchemy import Column, Integer, DateTime, Boolean
from models.db import db

class BaseModel(db.Model):
    __abstract__ = True  # Bu sınıf bir temel sınıf olduğu için tabloya karşılık gelmez

    IsDeleted = Column(Boolean, default=False)
    CreatedDate = Column(DateTime)
    CreatedBy = Column(Integer)
    ChangedDate = Column(DateTime)
    ChangedBy = Column(Integer)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.Id})>"
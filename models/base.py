from sqlalchemy import Column, Boolean, DateTime, func
from models.db import db

class BaseModel(db.Model):
    __abstract__ = True

    IsDeleted = Column(Boolean, default=False)
    CreatedDate = Column(DateTime, default= func.now())
    ChangedDate = Column(DateTime, default=func.now(), onupdate=func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        self.IsDeleted = True
        db.session.commit()

    def to_dict(self):
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return columns

from sqlalchemy import Column, Integer, Boolean, DateTime
from models.db import db

DEFAULT_USER_ID = 1  # Varsayılan kullanıcı ID'si (Geliştirme aşamasında sabit kullanıcı)

class BaseModel(db.Model):
    __abstract__ = True  # Bu sınıf bir temel sınıf olduğu için tabloya karşılık gelmez

    IsDeleted = Column(Boolean, default=False)
    CreatedDate = Column(DateTime, default=db.func.current_timestamp())
    CreatedBy = Column(Integer, default=DEFAULT_USER_ID)
    ChangedDate = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    ChangedBy = Column(Integer, default=DEFAULT_USER_ID)

    def save(self, created_by=DEFAULT_USER_ID):
        """Yeni bir nesne kaydedildiğinde CreatedBy ve ChangedBy otomatik olarak atanır."""
        if not self.CreatedBy:
            self.CreatedBy = created_by
        self.ChangedBy = created_by
        db.session.add(self)
        db.session.commit()

    def update(self, changed_by=DEFAULT_USER_ID):
        """Var olan bir nesneyi güncellerken ChangedBy otomatik olarak atanır."""
        self.ChangedBy = changed_by
        db.session.commit()

    def delete(self):
        """Silme işlemi yerine IsDeleted flag'ını kullanarak soft delete işlemi yapılır."""
        self.IsDeleted = True
        db.session.commit()

    def to_dict(self):
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return columns

from .db import db  # db'yi artık buradan import ediyoruz

class Speaker(db.Model):
    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.String(500))

    def __repr__(self):
        return f"<Speaker {self.first_name} {self.last_name}>"

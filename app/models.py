from . import db
from datetime import datetime

class Movie(db.Model):
    __tablename__ = 'movies'  # Nombre de la tabla

    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.SmallInteger, nullable=False)
    release = db.Column(db.Date, nullable=False)

    def __init__(self, id, title, duration, release):
        self.id = id
        self.title = title
        self.duration = duration
        self.release = release

    def to_dict(self):
        """Convierte el objeto Movie en un diccionario para facilitar el uso en JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "duration": self.duration,
            "release": self.release.isoformat(),
        }

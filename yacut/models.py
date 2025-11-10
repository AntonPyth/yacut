from datetime import datetime

from yacut import db

from .constants import URL_PREFIX


class URLMap(db.Model):
    """Модель для ссылки."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    def to_dict(self):
        return {'url': self.original,
                'short_link': f'{URL_PREFIX}{self.short}'}
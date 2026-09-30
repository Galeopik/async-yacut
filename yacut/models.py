from datetime import datetime

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True, comment='Идентификатор')
    original = db.Column(db.String(256), nullable=False,
                         comment='Длинная ссылка')
    short = db.Column(db.String(64), nullable=False, comment='Короткая ссылка')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now(),
                          comment='Время создания')
from datetime import datetime
from random import choices

from flask import url_for

from yacut import db

from .constants import (LIMIT_REPEAT, MAX_LENGTH_ORIGINAL_LINK,
                        MAX_LENGTH_SHORT_LINK, REDIRECT_ENDPOINT,
                        RESERVED_NAME, SHORT_CHARS, SHORT_ID_PATTERN,
                        SHORT_LENGTH)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True, comment='Идентификатор')
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL_LINK), nullable=False,
                         comment='Длинная ссылка')
    short = db.Column(db.String(MAX_LENGTH_SHORT_LINK), nullable=False,
                      comment='Короткая ссылка')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now,
                          comment='Время создания')

    @staticmethod
    def get_unique_short_id():
        for _ in range(LIMIT_REPEAT):
            short = ''.join(choices(SHORT_CHARS, k=SHORT_LENGTH))
            if (
                not URLMap.query.filter_by(short=short).first()
                and short != RESERVED_NAME
            ):
                break
        return short

    @classmethod
    def get_url_map_by_short(cls, short):
        return cls.query.filter_by(short=short).first()

    @classmethod
    def create(cls, original, short):
        if not short:
            short = cls.get_unique_short_id()

        if (
            cls.get_url_map_by_short(short=short)
            or short in RESERVED_NAME
        ):
            return None

        url_map = cls(
            original=original,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def is_valid_short(short):
        return SHORT_ID_PATTERN.fullmatch(short) is not None

    def get_short_link(self):
        return url_for(
            REDIRECT_ENDPOINT,
            short=self.short,
            _external=True
        )
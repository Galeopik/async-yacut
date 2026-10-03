from datetime import datetime
from random import choices

from flask import url_for

from . import db
from .constants import (LIMIT_REPEAT_CREATE_SHORT, MAX_LENGTH_ORIGINAL_LINK,
                        MAX_LENGTH_SHORT, REDIRECT_ENDPOINT, RESERVED_NAME,
                        SHORT_CHARS, SHORT_LENGTH, SHORT_PATTERN)
from .error_handler import InvalidAPIUsageError


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True, comment='Идентификатор')
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL_LINK), nullable=False,
                         comment='Длинная ссылка')
    short = db.Column(db.String(MAX_LENGTH_SHORT), nullable=False,
                      comment='Короткая ссылка')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now,
                          comment='Время создания')

    @staticmethod
    def get_url_map_by_short(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short():
        for _ in range(LIMIT_REPEAT_CREATE_SHORT):
            short = ''.join(choices(SHORT_CHARS, k=SHORT_LENGTH))
            if (
                short != RESERVED_NAME
                and not URLMap.get_url_map_by_short(short)
            ):
                return short
        raise RuntimeError(
            'Не удалось сгенерировать уникальный короткий идентификатор'
        )

    @staticmethod
    def create(original, short, validate_short=True, validate_original=True):
        if validate_original and len(original) > MAX_LENGTH_ORIGINAL_LINK:
            raise InvalidAPIUsageError(
                'Исходная ссылка слишком длинная'
            )

        if not short:
            short = URLMap.get_unique_short()

        elif validate_short and (
            not SHORT_PATTERN.fullmatch(short)
            or len(short) > MAX_LENGTH_SHORT
        ):
            raise InvalidAPIUsageError(
                'Указано недопустимое имя для короткой ссылки'
            )
        if (
            URLMap.get_url_map_by_short(short=short)
            or short == RESERVED_NAME
        ):
            raise InvalidAPIUsageError(
                'Предложенный вариант короткой ссылки уже существует.'
            )

        url_map = URLMap(
            original=original,
            short=short
        )
        db.session.add(url_map)
        return url_map

    def get_short_link(self):
        return url_for(
            REDIRECT_ENDPOINT,
            short=self.short,
            _external=True
        )
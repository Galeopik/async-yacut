from datetime import datetime
from random import choices

from flask import url_for

from . import db
from .constants import (LIMIT_REPEAT_CREATE_SHORT, MAX_LENGTH_ORIGINAL_LINK,
                        MAX_LENGTH_SHORT, REDIRECT_ENDPOINT, RESERVED_SHORT,
                        SHORT_CHARS, SHORT_LENGTH, SHORT_PATTERN)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True, comment='Идентификатор')
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL_LINK), nullable=False,
                         comment='Длинная ссылка')
    short = db.Column(db.String(MAX_LENGTH_SHORT), nullable=False,
                      comment='Короткая ссылка')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now,
                          comment='Время создания')

    @staticmethod
    def is_short_reserved(short):
        return short == RESERVED_SHORT or URLMap.get(short=short)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short():
        for _ in range(LIMIT_REPEAT_CREATE_SHORT):
            short = ''.join(choices(SHORT_CHARS, k=SHORT_LENGTH))
            if not URLMap.is_short_reserved(short):
                return short
        raise RuntimeError(
            f'Не удалось сгенерировать уникальный короткий идентификатор '
            f'Попыток: {LIMIT_REPEAT_CREATE_SHORT}.'
        )

    @staticmethod
    def create(
        original,
        short=None,
        validate_short=True,
        validate_original=True,
        commit=True
    ):
        if validate_original and len(original) > MAX_LENGTH_ORIGINAL_LINK:
            raise ValueError(
                f'Исходная ссылка слишком длинная. '
                f'Длина должна быть не более {MAX_LENGTH_ORIGINAL_LINK}'
            )

        if not short:
            short = URLMap.get_unique_short()

        else:
            if validate_short and (
                not SHORT_PATTERN.fullmatch(short)
                or len(short) > MAX_LENGTH_SHORT
            ):
                raise ValueError(
                    'Указано недопустимое имя для короткой ссылки'
                )
            if URLMap.is_short_reserved(short):
                raise ValueError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )

        url_map = URLMap(
            original=original,
            short=short
        )
        db.session.add(url_map)
        if commit:
            db.session.commit()
        return url_map

    def get_short_link(self):
        return url_for(
            REDIRECT_ENDPOINT,
            short=self.short,
            _external=True
        )
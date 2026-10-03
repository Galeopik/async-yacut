from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (INVALID_SHORT_MESSAGE, MAX_LENGTH_ORIGINAL_LINK,
                        MAX_LENGTH_SHORT, SHORT_PATTERN)

ORIGINAL_LINK_LABEL = 'Введите длинную ссылку'
SHORT_LABEL = 'Ваш вариант короткой ссылки'
REQUIRED_MESSAGE = 'Обязательное поле'
SUBMIT_LABEL = 'Создать'


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_LABEL,
        validators=[DataRequired(message=REQUIRED_MESSAGE),
                    Length(max=MAX_LENGTH_ORIGINAL_LINK)]
    )
    custom_id = URLField(
        SHORT_LABEL,
        validators=[
            Optional(),
            Length(max=MAX_LENGTH_SHORT),
            Regexp(
                SHORT_PATTERN,
                message=INVALID_SHORT_MESSAGE
            )
        ]
    )
    submit = SubmitField(SUBMIT_LABEL)


class FileForm(FlaskForm):
    files = MultipleFileField(
        validators=[DataRequired(message=REQUIRED_MESSAGE)]
    )
    submit = SubmitField(SUBMIT_LABEL)

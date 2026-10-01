from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from .constants import (CUSTOM_ID_LABEL, MAX_LENGTH_ORIGINAL_LINK,
                        ORIGINAL_LINK_LABEL, REQUIRED_MESSAGE,
                        SHORT_ID_PATTERN, SUBMIT_LABEL)


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_LABEL,
        validators=[DataRequired(message=REQUIRED_MESSAGE),
                    Length(max=MAX_LENGTH_ORIGINAL_LINK)]
    )
    custom_id = URLField(
        CUSTOM_ID_LABEL,
        validators=[Optional()]
    )
    submit = SubmitField(SUBMIT_LABEL)

    def validate_custom_id(self, custom_id):
        if not SHORT_ID_PATTERN.fullmatch(custom_id.data):
            raise ValidationError(
                'Указано недопустимое имя для короткой ссылки'
            )


class FileForm(FlaskForm):
    files = MultipleFileField(
        validators=[DataRequired(message=REQUIRED_MESSAGE)]
    )
    submit = SubmitField(SUBMIT_LABEL)

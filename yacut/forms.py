from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Введите длинную ссылку',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 256)]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Optional(), Length(1, 16)]
    )
    submit = SubmitField('Создать')


class FileForm(FlaskForm):
    files = MultipleFileField(
        'Файлы',
        validators=[DataRequired(message='Обязательное поле')]
    )
    submit = SubmitField('Создать')
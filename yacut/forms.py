from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class LinkForm(FlaskForm):
    """Форма для создания короткой ссылки."""

    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(max=16, message='Не более 16 символов'),
            Optional(),
            Regexp(
                r'^[A-Za-z0-9]+$',
                message='Можно только маленькие и большие лат. буквы, цифры'
            )
        ])
    submit = SubmitField('Создать')

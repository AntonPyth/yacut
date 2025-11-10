from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_short_id_list, get_unique_short_id, validate_custom_id


@app.route('/api/id', methods=['POST'])
def generate_short_link():
    """Генерирует короткую ссылку вместо длинной."""
    if not request.data:
        """
        >>> если менять на if request.data is None:
        >>> тесты падают Проверил в интернете, так делать неверно.
        """
        raise InvalidAPIUsage('Отсутствует тело запроса')
    data = request.get_json(silent=True)
    if not data or 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    custom_id = data.get('custom_id')
    if not custom_id:
        short_id = get_unique_short_id()
    else:
        short_id = custom_id
        if not validate_custom_id(short_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if short_id in get_short_id_list():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
    link = URLMap(original=data['url'], short=short_id)
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>')
def get_original_link(short_id):
    """Возвращает первоначальную ссылку."""
    link = URLMap.query.filter_by(short=short_id).first()
    if link is not None:
        return jsonify({'url': link.original}), HTTPStatus.OK
    raise InvalidAPIUsage(
        'Указанный id не найден', HTTPStatus.NOT_FOUND
    )

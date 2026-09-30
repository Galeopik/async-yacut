import re

from flask import jsonify, request, url_for

from . import app, db
from .error_handler import InvalidAPIUsageError
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsageError(
            'Указанный id не найден',
            404
        )
    return jsonify({'url': url.original}), 200


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsageError('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsageError('\"url\" является обязательным полем!')
    if 'custom_id' not in data or data['custom_id'] == '':
        data['custom_id'] = get_unique_short_id()
    if not re.fullmatch(r'[A-Za-z0-9]{1,16}', data['custom_id']):
        raise InvalidAPIUsageError(
            'Указано недопустимое имя для короткой ссылки'
        )
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsageError(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    url = URLMap(
        original=data['url'],
        short=data['custom_id']
    )
    db.session.add(url)
    db.session.commit()
    return jsonify({
        'url': url.original,
        'short_link': url_for(
            'redirect_to_original',
            short_code=url.short,
            _external=True
        )
    }), 201

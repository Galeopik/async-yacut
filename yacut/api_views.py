from flask import jsonify, request

from . import app
from .constants import ERROR_404, STATUS_CREATED, STATUS_SUCCESS
from .error_handler import InvalidAPIUsageError
from .models import URLMap


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.get_url_map_by_short(short_id)
    if not url_map:
        raise InvalidAPIUsageError(
            'Указанный id не найден',
            ERROR_404
        )
    return jsonify({'url': url_map.original}), STATUS_SUCCESS


@app.route('/api/id/', methods=['POST'])
def create_short_link_api():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsageError('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsageError('"url" является обязательным полем!')
    if 'custom_id' not in data or data['custom_id'] == '':
        data['custom_id'] = URLMap.get_unique_short_id()
    if not URLMap.is_valid_short(data['custom_id']):
        raise InvalidAPIUsageError(
            'Указано недопустимое имя для короткой ссылки'
        )
    if URLMap.get_url_map_by_short(short=data['custom_id']) is not None:
        raise InvalidAPIUsageError(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    url_map = URLMap.create(
        original=data['url'],
        short=data['custom_id']
    )
    return jsonify({
        'url': url_map.original,
        'short_link': url_map.get_short_link()
    }), STATUS_CREATED

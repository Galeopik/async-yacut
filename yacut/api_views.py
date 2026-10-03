from flask import jsonify, request

from . import app
from .constants import ERROR_404, STATUS_CREATED
from .error_handler import InvalidAPIUsageError
from .models import URLMap


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    url_map = URLMap.get(short)
    if not url_map:
        raise InvalidAPIUsageError(
            'Указанный id не найден',
            ERROR_404
        )
    return jsonify({'url': url_map.original})


@app.route('/api/id/', methods=['POST'])
def create_short_link_api():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsageError('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsageError('"url" является обязательным полем!')
    try:
        return jsonify({
            'url': data['url'],
            'short_link': URLMap.create(
                original=data['url'],
                short=data.get('custom_id')
            ).get_short_link()
        }), STATUS_CREATED
    except Exception as error:
        raise InvalidAPIUsageError(str(error))

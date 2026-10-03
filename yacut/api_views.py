from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from . import app, db
from .constants import ERROR_404, STATUS_CREATED
from .error_handler import InvalidAPIUsageError
from .models import URLMap


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.get_url_map_by_short(short=short_id)
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
    if 'custom_id' not in data or data['custom_id'] == '':
        data['custom_id'] = URLMap.get_unique_short()
    try:
        short_link = URLMap.create(
            original=data['url'],
            short=data['custom_id']
        ).get_short_link()

        db.session.commit()

        return jsonify({
            'url': data['url'],
            'short_link': short_link
        }), STATUS_CREATED

    except IntegrityError as error:
        raise InvalidAPIUsageError(
            f'Ошибка при создании в БД: {error}'
        )
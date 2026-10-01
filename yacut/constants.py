import re
import string

LIMIT_REPEAT = 100
SHORT_CHARS = string.ascii_letters + string.digits
SHORT_LENGTH = 6
ERROR_404 = 404
ERROR_400 = 400
RESERVED_NAME = ('files', 'api', 'admin')
MAX_LENGTH_ORIGINAL_LINK = 8192
MAX_LENGTH_SHORT_LINK = 16
REDIRECT_ENDPOINT = 'redirect_to_original'
ORIGINAL_LINK_LABEL = 'Введите длинную ссылку'
CUSTOM_ID_LABEL = 'Ваш вариант короткой ссылки'
REQUIRED_MESSAGE = 'Обязательное поле'
SUBMIT_LABEL = 'Создать'
STATUS_SUCCESS = 200
STATUS_CREATED = 201
SHORT_ID_PATTERN = re.compile(
    rf'[{re.escape(SHORT_CHARS)}]{{1,{MAX_LENGTH_SHORT_LINK}}}'
)

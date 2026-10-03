import re
import string
from http import HTTPStatus

ERROR_404 = HTTPStatus.NOT_FOUND
ERROR_400 = HTTPStatus.BAD_REQUEST
STATUS_CREATED = HTTPStatus.CREATED
LIMIT_REPEAT_CREATE_SHORT = 100
SHORT_CHARS = string.ascii_letters + string.digits
SHORT_LENGTH = 6
RESERVED_NAME = 'files'
MAX_LENGTH_ORIGINAL_LINK = 8192
MAX_LENGTH_SHORT = 16
REDIRECT_ENDPOINT = 'redirect_to_original'
ORIGINAL_LINK_LABEL = 'Введите длинную ссылку'
CUSTOM_ID_LABEL = 'Ваш вариант короткой ссылки'
REQUIRED_MESSAGE = 'Обязательное поле'
INVALID_SHORT_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
SUBMIT_LABEL = 'Создать'
SHORT_PATTERN = re.compile(
    rf'[{re.escape(SHORT_CHARS)}]+'
)

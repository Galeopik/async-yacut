import re
import string
from http import HTTPStatus

ERROR_404 = HTTPStatus.NOT_FOUND
ERROR_400 = HTTPStatus.BAD_REQUEST
STATUS_CREATED = HTTPStatus.CREATED
LIMIT_REPEAT_CREATE_SHORT = 100
SHORT_CHARS = string.ascii_letters + string.digits
SHORT_LENGTH = 6
RESERVED_SHORT = 'files'
MAX_LENGTH_ORIGINAL_LINK = 8192
MAX_LENGTH_SHORT = 16
REDIRECT_ENDPOINT = 'redirect_to_original'
INVALID_SHORT_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
SHORT_PATTERN = re.compile(
    rf'[{re.escape(SHORT_CHARS)}]+'
)

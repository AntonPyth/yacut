from random import choices

from .constants import (
    CHARACTERS, SHORT_LINK_LENGTH
)
from .models import URLMap


def get_short_id_list():
    short_id_list = [short[0]
                     for short
                     in URLMap.query.with_entities(URLMap.short).all()]
    short_id_list.append('files')
    return short_id_list


def get_unique_short_id():
    """Формирует короткий индикатор для ссылки."""
    short_id_list = get_short_id_list()
    short_id = ''.join(choices(CHARACTERS, k=SHORT_LINK_LENGTH))
    while short_id in short_id_list:
        short_id = ''.join(choices(CHARACTERS, k=SHORT_LINK_LENGTH))
    return short_id


def validate_custom_id(custom_id):
    """Проверяет, что короткая ссылка пользователя удовлетворяет условиям."""
    if len(custom_id) not in range(1, 17):
        return False
    if set(custom_id) - set(CHARACTERS):
        return False
    return True

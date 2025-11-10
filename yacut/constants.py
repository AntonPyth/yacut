from string import ascii_letters, digits

from . import app

CHARACTERS = list(ascii_letters + digits)
SHORT_LINK_LENGTH = 6

URL_PREFIX = 'http://localhost:5000/'
SHORT_PREFIX = 'short/'

API_VERSION = 'v1'

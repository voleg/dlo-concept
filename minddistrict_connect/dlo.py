import hashlib
import hmac
import uuid
from datetime import datetime
from urllib.parse import urlencode, urljoin

# ruff: noqa: S101


USER_RESOURSES = {
    'client': {
        'catalogue': 'client catalog',
        'conversations': 'conversations',
    },

    'careprovider': {
        'tasks': 'tasks for professional',
        'c': 'my clients',
        'c/@@allclients': 'all clients',
        'p': 'list of proffessionals',
        'configuration': 'application configuration',
        'catalogue': 'client catalog',
    }
}


def build_hmac_token(secret_key: str, message: str) -> str:
    """Generate HMAC token using SHA-512 algorithm."""
    key = secret_key.encode('ascii')
    message_encoded = message.encode('ascii')
    return hmac.new(key, message_encoded, hashlib.sha512).hexdigest()


class DLOAdapter:
    def __init__(self,
                 secret_key: str, base_url: str, usertype:
                 str, userid: str) -> None:

        self.secret_key = secret_key
        self.base_url = base_url
        self.usertype = usertype
        self.userid = userid

    def get_nonce(self) -> str:
        return str(uuid.uuid4())

    def get_utc_timestamp(self) -> str:
        return datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'

    def get_params(self) -> dict:
        return {
            'nonce': self.get_nonce(),
            'timestamp': self.get_utc_timestamp(),
            'userid': self.userid,
            'usertype': self.usertype,
        }

    def build_message(self, **params) -> str:
        return ''.join([key + str(value) for key, value in sorted(params.items())])

    def build_url(self, path: str = '', redirect: str = None):
        base_url = urljoin(self.base_url, path)
        params = self.get_params()

        if redirect:
            params['redirect'] = redirect
            base_url = urljoin(self.base_url, 'aux/frameredirect')

        message = self.build_message(**params)
        token = build_hmac_token(self.secret_key, message)
        params.update({'token': token})
        query_string = urlencode(params)

        return f'{base_url}/?{query_string}'

    def discover_resources(self, usertype: str) -> dict[str, str] | None:
        return USER_RESOURSES.get(usertype)


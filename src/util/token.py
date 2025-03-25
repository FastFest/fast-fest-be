from datetime import datetime, timedelta

from jwt import encode, decode

from util.config import config


def jwt_decoder(token: str):
    payload = decode(token, config.JWT_SECRET_KEY, algorithms=['HS256'])
    return payload['data']['user_id']


def access_token_gen(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=40),
        'iat': datetime.utcnow(),
        'scope': 'access_token',
        'data': {
            'user_id': user_id,
        }
    }
    access_token = encode(
        payload,
        config.JWT_SECRET_KEY,
        algorithm='HS256'
    )
    return access_token

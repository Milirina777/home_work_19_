from flask import request
from flask import abort
import jwt
from constants import SECRET, ALGO


def auth_required(func):
    """Ограничивает доступ к некоторым эндпоинтам для запросов без токена"""
    def wrappers(*args, **kwargs):
        data = request.headers
        if 'Authorization' not in request.headers:
            abort(401)

        token_data = data.get('Authorization')
        token = token_data.split('Bearer ')[-1]

        try:
            jwt.decode(token, key=SECRET, algorithms=[ALGO])
            return func(*args, **kwargs)
        except Exception as e:
            print("Authorisation error", e)
            abort(401)
        return func(*args, **kwargs)

    return wrappers


def admin_required(func):
    """Ограничивает доступ на редактирование другим пользователям, но не для администраторов"""
    def wrappers(*args, **kwargs):
        data = request.headers

        if 'Authorization' not in data:
            abort(401)

        token_data = data.get('Authorization')
        token = token_data.split('Bearer ')[-1]

        try:
            user_data = jwt.decode(token, key=SECRET, algorithms=[ALGO])
        except Exception as e:
            print("Admin authorisation error", e)
            abort(401)
        else:
            if user_data["role"] != 'admin':
                return func(*args, **kwargs)
        abort(403)

    return wrappers

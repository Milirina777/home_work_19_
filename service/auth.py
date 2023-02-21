import calendar
import datetime
import jwt

from constants import SECRET, ALGO
from service.user import UserService, password_check


def new_token(token):
    """Создание и проверка токена"""
    try:
        token_data = jwt.decode(token.get('refresh_token'), key=SECRET, algorithms=[ALGO])
        return token_data
    except Exception as e:
        print("Decoding error", e)
        return False

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_token(self, username, password, is_refresh=False):
        """Генерация токена для пользователя"""
        user_info = self.user_service.get_user_by_username(username)

        if user_info is None:
            return "User is not exist!", 403

        if not is_refresh:
            if not password_check(user_info.password, password):
                return "Password is incorrect", 403

        token_data = {'username': user_info.user_name,
                      'role': user_info.role,
                      }

        # 30 минут жизни для access_token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token_data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(token_data, SECRET, algorithm=[ALGO])

        # 60 дней жизни для refresh_token
        days60 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        token_data["exp"] = calendar.timegm(days60.timetuple())
        refresh_token = jwt.encode(token_data, SECRET, algorithm=[ALGO])

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def check_token(self, refresh_token):
        """Проверка валидности токена"""
        token_data = jwt.decode(jwt=refresh_token, key=SECRET, algorithms=[ALGO])
        username = token_data.get("username")
        user_info = self.user_service.get_user_by_username(username)

        return self.get_token(username, user_info.password, is_refresh=True)

import base64
import hashlib
import hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO

class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def get_user_by_username(self, username):
        return self.dao.get_user_by_name(username)

    def create(self, user_d):
        user_d["password"] = get_hash(user_d.get["password"])
        return self.dao.create(user_d)

    def update(self, user_d):
        user_d["password"] = get_hash(user_d["password"])
        self.dao.update(user_d)

    def delete(self, uid):
        self.dao.delete(uid)

def get_hash(password):
    """Генерация хэша для пароля пользователя"""
    hash_digest = hashlib.pbkdf2_hmac(
        'HS256',
        password.encode('utf-8'),
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    )
    return base64.b64encode(hash_digest)

def password_check(hash_pass, password_hash):
    """Сверка пароля и хэша"""
    hash_dig = base64.b64encode(hash_pass)
    check_pass = hashlib.pbkdf2_hmac(
        'HS256',
        password_hash.encode('utf-8'),
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    )

    return hmac.compare_digest(hash_dig, check_pass)
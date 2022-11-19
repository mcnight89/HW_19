import base64
import hashlib
import hmac

from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_user_by_username(self, username):
        return self.dao.get_user_by_username(username)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user):
        password = user.get("password")
        hashed_password = self.generate_password(password)
        user['password'] = hashed_password
        self.dao.create(user)

    def update(self, user, username):
        user['password'] = self.generate_password(user["password"])
        return self.dao.update(user, username)

    def delete(self, uid):
        self.dao.delete(uid)

    def generate_password(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return base64.b64encode(hash_digest)

    def compare_password(self, password_hash, other_password):
        hashed_password = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        decode_password = base64.b64encode(password_hash)
        return hmac.compare_digest(decode_password, hashed_password)

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

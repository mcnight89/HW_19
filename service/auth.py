import calendar
import datetime

import jwt
from flask import abort
from constants import JWT_SECRET, JWT_ALGORITHM


class AuthService:
    def __init__(self, user_service):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_user_by_username(username)
        if user is None:
            abort(401)

        if not is_refresh:
            if not self.user_service.compare_password(user.password, password):
                abort(401)
        data = {
            "username": user.username,
            "role": user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens, 201

    def approve_refresh_token(self, refresh_token):
        try:
            user_data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithm=[JWT_ALGORITHM])
            user_name = user_data.get('username')
            return self.generate_tokens(user_name, None, is_refresh=True)
        except Exception as e:
            abort(401)

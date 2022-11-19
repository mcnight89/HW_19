from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from decorators import admin_required, auth_required
from implemented import user_service

user_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/<username>')
class UserView(Resource):
    @admin_required
    def get(self, username):
        user = user_service.get_user_by_username(username)
        return user_schema.dump(user), 200

    @admin_required
    def delete(self, username):
        try:
            user_service.delete(username)
            return "user deleted", 201
        except Exception as e:
            return 404

    @auth_required
    def put(self, username):
        req_json = request.json
        user_service.update(req_json, username)
        return "user updated", 201


@user_ns.route('/')
class UserView(Resource):
    def get(self):
        users = user_service.get_all()
        return users_schema.dump(users)

    def post(self):
        req_json = request.json
        user_service.create(req_json)
        return "user created", 201

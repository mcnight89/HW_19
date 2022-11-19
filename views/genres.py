from flask_restx import Resource, Namespace
from flask import request

from dao.model.genre import GenreSchema
from implemented import genre_service
from decorators import admin_required, auth_required

genre_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        try:
            genre = genre_service.get_all()
            return genres_schema.dump(genre), 200
        except Exception as e:
            return 404

    @admin_required
    def post(self):
        try:
            req_json = request.json
            genre_service.create(req_json)
            return "genre added", 201
        except Exception as e:
            return 404


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid: int):
        try:
            genre = genre_service.get_one(gid)
            return genre_schema.dump(genre), 200
        except Exception as e:
            return "genre not found"

    @admin_required
    def put(self, gid):
        try:
            req_json = request.json
            req_json['id'] = gid
            genre_service.update(req_json)
            return "genres updated", 201
        except Exception as e:
            return "genre not updated", 404

    @admin_required
    def delete(self, gid):
        try:
            genre_service.delete(gid)
            return "data deleted", 204
        except Exception as e:
            return "data not found", 404


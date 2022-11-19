from flask_restx import Resource, Namespace
from flask import request

from dao.model.movie import MovieSchema
from implemented import movie_service
from decorators import admin_required, auth_required

movie_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    @auth_required
    def get(self):
        try:
            director = request.args.get('director_id')
            genre = request.args.get('genre')
            year = request.args.get('year')
            filters = {
                "director_id": director,
                "genre_id": genre,
                "year": year
            }
            movie = movie_service.get_all()
            return movies_schema.dump(movie), 200
        except Exception as e:
            return 404

    @admin_required
    def post(self):
        try:
            req_json = request.json
            movie_service.create(req_json)
            return "movie added", 201
        except Exception as e:
            return 404


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    @auth_required
    def get(self, mid: int):
        try:
            movie = movie_service.get_one(mid)
            return movie_schema.dump(movie), 200
        except Exception as e:
            return "movie not found"

    @admin_required
    def put(self, mid):
        try:
            req_json = request.json
            req_json['id'] = mid
            movie_service.update(req_json)
            return "movies updated", 201
        except Exception as e:
            return "movie not updated", 404

    @admin_required
    def delete(self, mid):
        try:
            movie_service.delete(mid)
            return "data deleted", 204
        except Exception as e:
            return "data not found", 404

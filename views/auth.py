from flask_restx import Namespace, Resource
from flask import request, abort
from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        data = request.json

        username = data.get('username', None)
        password = data.get('password', None)

        if None in [username, password]:
            return abort(400)

        token_data = auth_service.get_token(username, password)
        return token_data, 201


    def put(self):
        new_token = request.json
        token = new_token.get('refresh_token', None)
        if token is None:
            return abort(400)

        token_data = auth_service.check_token(token)

        return token_data, 201

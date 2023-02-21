from flask import request
from flask_restx import Namespace, Resource

from dao.model.user import UserSchema
from implemented import user_service

users_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_ns.route('/')
class UsersView(Resource):
    def get(self):

        users = user_service.get_all()
        output_us = users_schema.dump(users)

        return output_us, 200

    def post(self):

        data = request.json
        user = user_service.create(data)

        return "Posted", 201, {"location": f"/user/{user.id}"}


@users_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        result = user_schema.dump(user)
        return result, 200

    def post(self, uid):
        req_json = request.json

        if 'id' not in req_json:
            req_json['id'] = uid

        user_service.update(req_json)

    def delete(self, uid):
        user_data = user_service.delete(uid)
        result = user_schema.dump(user_data)
        return result, 'Information is deleted', 204

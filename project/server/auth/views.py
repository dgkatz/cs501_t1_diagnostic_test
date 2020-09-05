# project/server/auth/views.py

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import User

auth_blueprint = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def get(self):
    	responseObject = {
    		'status': 'success',
    		'message': 'Request successful but please send an HTTP POST request to register the user.'
    	}
    	return make_response(jsonify(responseObject)), 200

    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )

                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202


class UsersListAPI(MethodView):
    """
    Users List Resource
    """

    def get(self):
        users = User.query.all()
        response = []
        for user in users:
            response.append({
                "email": user.email,
                "is_admin": user.admin,
                "registered_on": user.registered_on
            })
        return make_response(jsonify(response)), 200


# define the API resources
registration_view = RegisterAPI.as_view('register_api')
user_list_view = UsersListAPI.as_view('user_list_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST', 'GET']
)

auth_blueprint.add_url_rule(
    '/users/index',
    view_func=user_list_view,
    methods=['GET']
)

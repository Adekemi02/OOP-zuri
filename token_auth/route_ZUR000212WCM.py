import os
import jwt
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from .db import User
from http import HTTPStatus
from functools import wraps
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


#   Namespace
token_ns = Namespace('token', description='Token Authentication')

#   User model
users_model = token_ns.model(
    'User', {
        'username': fields.String(required=True, description='Username'),
        'email': fields.String(required=True, description='User email address'),
        'password': fields.String(required=True, description='User password')
    }
)

login_model = token_ns.model(
    'Login', {
        'email': fields.String(required=True),
        'password': fields.String(required=True)
    }
)

#   This function generates token
# def generate_token(email):
#     token = jwt.encode({'email': email}, os.environ.get('SECRET_KEY'), algorithm='HS256')
#     return token

#   Token validation decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), HTTPStatus.UNAUTHORIZED

        try:
            data = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
            current_user = data.get('email')
        except:
            return jsonify({'message': 'Token is invalid'}), HTTPStatus.UNAUTHORIZED

        return f(current_user, *args, **kwargs)

    return decorated


#   Register route
@token_ns.route("/register")
class RegisterUser(Resource):
    @token_ns.expect(users_model)
    @token_ns.doc(description='Register a new user')
    def post(self):
        '''
            Register a user
        '''
        data = request.get_json()

        email = data.get("email")

        user = User.get_by_email(email)

        if user:
            return {"message": "User already exits!"}, HTTPStatus.CONFLICT
        
        new_user = User(
            username = data.get("username"),
            email = data.get("email"),
            password = generate_password_hash(data.get("password"))
        )

        new_user.save()

        return ({"message": "User created successfully"}), HTTPStatus.CREATED
    

@token_ns.route("/login")
class LoginUser(Resource):
    @token_ns.expect(login_model)
    @token_ns.doc(description='Login a user',
                  params = {'email': 'User email address',
                            'password': 'User password'})
    def post(self):
        '''
            Login a user
        '''
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {'message': 'Email and password required'}, HTTPStatus.BAD_REQUEST

        user = User.get_by_email(email)

        if user and check_password_hash(user.password, password):
            # token = generate_token(user)
            token_data = {
                'sub': 'user_id',
                'identity': user.email
            }

            token = jwt.encode(token_data,
                               os.getenv('SECRET_KEY'), algorithm="HS256")
            
            if not token:
                return {'message': 'Invalid token'}, HTTPStatus.NOT_FOUND
            
            response = {
                "message": "User logged in successfully",
                "token": token
                # "token": jwt.decode(token,
                #                     os.getenv('SECRET_KEY'), algorithms='HS256')
            }
            
            return response, HTTPStatus.OK
        
        return {'message': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
        

@token_ns.route('/home')
class GetAllUsers(Resource):
    @token_ns.marshal_list_with(users_model)
    @token_ns.doc(description='Get all users')
    def get(self):
        '''
            Get all users
        '''
        token = request.headers.get('Authorization')

        if not token:
            return {"message": "Token is missing"}, HTTPStatus.NOT_FOUND
        
        try:
            data = jwt.decode(token,
                            os.getenv('SECRET_KEY'), algorithms='HS256')
            current_user = data.get('username')

            users=User.query.all()

            return users, HTTPStatus.OK
        
        except jwt.ExpiredSignatureError:
            return {"message": "Token has expired"}, HTTPStatus.UNAUTHORIZED
        
        except jwt.InvalidTokenError:
            return {"message": "Invalid token"}, HTTPStatus.UNAUTHORIZED


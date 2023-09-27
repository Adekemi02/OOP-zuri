from flask import Flask
from flask_restx import Api
import os
import jwt
from .route_ZUR000212WCM import token_ns
from dotenv import load_dotenv, find_dotenv
from .db import db, User


load_dotenv(find_dotenv())

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(BASE_DIR, "db.sqlite3")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True
    app.debug = os.environ.get('FLASK_DEBUG')

    db.init_app(app)

    api = Api(app,
          title="Token Authorization")

    api.add_namespace(token_ns, path='/api/v1')

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "User": User
        }


    return app


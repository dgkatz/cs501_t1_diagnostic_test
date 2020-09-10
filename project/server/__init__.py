# project/server/__init__.py

import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import flask_migrate

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

migrate = flask_migrate.Migrate(
    db=db, directory="../migrations", render_as_batch=False
)

migrate.init_app(app)

with app.app_context():
    migrate.upgrade()

from project.server.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)
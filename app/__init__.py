import os
from flask import Flask
from .config import DevelopmentConfig, TestingConfig, ProductionConfig
from .extensions import register_extensions
from .api import register_api_blueprint


def create_app(config_object=None) -> Flask:
    app = Flask(__name__, instance_relative_config=False)

    env = os.environ.get("FLASK_ENV", "production")

    if config_object:
        app.config.from_object(config_object)
    elif env == "development":
        app.config.from_object(DevelopmentConfig)
    elif env == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(ProductionConfig)

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("SQLALCHEMY_DATABASE_URI is not set")

    register_extensions(app)
    register_api_blueprint(app)

    @app.route("/")
    def index():
        return app.config.get("WELCOME_MESSAGE", "legendary api")

    return app

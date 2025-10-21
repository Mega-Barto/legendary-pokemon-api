from flask import Flask
from .config import Config
from .extensions import register_extensions
from .api import register_api_blueprint


def create_app(config_object: str | Config = "app.config.Config") -> Flask:
    """Application factory. Pass either a config object or import string.

    Returns a configured Flask app instance.
    """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_object)

    # register extensions, blueprints, error handlers, etc.
    register_extensions(app)
    register_api_blueprint(app)

    @app.route("/")
    def index():
        return app.config.get("WELCOME_MESSAGE", "legendary api")

    return app

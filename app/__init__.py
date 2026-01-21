import os
from flask import Flask
from .config import DevelopmentConfig, TestingConfig, ProductionConfig
from .extensions import register_extensions
from .api import register_api_blueprint
from flask_cors import CORS

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
    CORS(app)

    @app.route("/")
    def index():
        from flask import send_from_directory
        return send_from_directory(app.static_folder, 'index.html')

    return app

from flask import Blueprint


api_bp = Blueprint("api", __name__, url_prefix="/api")


def register_api_blueprint(app):
    from .routes import bp as routes_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(routes_bp)

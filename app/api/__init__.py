from flask import Blueprint

from .routes import register_routes

api_bp = Blueprint("api", __name__, url_prefix="/api")


def register_api_blueprint(app):
    """Register API blueprint and all route blueprints."""
    app.register_blueprint(api_bp)
    register_routes(app)


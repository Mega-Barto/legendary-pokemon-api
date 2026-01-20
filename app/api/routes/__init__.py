from .health import bp as health_bp
from .regions import bp as regions_bp
from .types import bp as types_bp
from .classifications import bp as classifications_bp
from .pokemon import bp as pokemon_bp
from .seed import bp as seed_bp

__all__ = [
    "health_bp",
    "regions_bp",
    "types_bp",
    "classifications_bp",
    "pokemon_bp",
    "seed_bp",
]


def register_routes(app):
    """Register all API route blueprints with the Flask app."""
    app.register_blueprint(health_bp)
    app.register_blueprint(regions_bp)
    app.register_blueprint(types_bp)
    app.register_blueprint(classifications_bp)
    app.register_blueprint(pokemon_bp)
    app.register_blueprint(seed_bp)


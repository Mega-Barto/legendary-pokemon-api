from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instantiate extensions here so other modules can import them.
db = SQLAlchemy()
migrate = Migrate()


def register_extensions(app):
    """Initialize Flask extensions with the app."""
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models  # noqa: F401

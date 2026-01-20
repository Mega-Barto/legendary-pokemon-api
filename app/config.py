import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration for the Flask app."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "please-change-me-in-production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(basedir, "..", "instance", "app.sqlite")
    )
    WELCOME_MESSAGE = "<p>legendary api</p>"


class DevelopmentConfig(Config):
    """Development configuration - uses SQLite locally."""
    ENV = "development"
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(basedir, "..", "instance", "dev.sqlite")
    )


class TestingConfig(Config):
    """Testing configuration - uses in-memory SQLite."""
    ENV = "testing"
    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    """Production configuration - requires MySQL via DATABASE_URL."""
    ENV = "production"
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


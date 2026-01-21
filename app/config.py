import os


class Config:
    """Base configuration for the Flask app."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "please-change-me-in-production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    WELCOME_MESSAGE = "<p>legendary api</p>"


class DevelopmentConfig(Config):
    """Development configuration - uses MySQL via Docker."""
    ENV = "development"
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://pokemon_user:pokemon_password@localhost:3306/legendary_pokemon_db"
    )


class TestingConfig(Config):
    """Testing configuration - uses separate test database."""
    ENV = "testing"
    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "mysql+pymysql://pokemon_user:pokemon_password@localhost:3306/legendary_pokemon_test"
    )


class ProductionConfig(Config):
    """Production configuration - requires MySQL via DATABASE_URL."""
    ENV = "production"
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


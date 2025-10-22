import os


class Config:
    """Base configuration for the Flask app."""
    ENV = "production"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "please-change-me-in-production")
    WELCOME_MESSAGE = "<p>legendary api</p>"
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///instance/app.sqlite"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    pass

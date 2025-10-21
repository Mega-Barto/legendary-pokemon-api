class Config:
    """Base configuration for the Flask app."""
    ENV = "production"
    DEBUG = False
    TESTING = False
    SECRET_KEY = "please-change-me-in-production"
    WELCOME_MESSAGE = "<p>legendary api</p>"


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    pass

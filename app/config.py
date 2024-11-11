import os


class Config:
    DEBUG = True
    PRODUCTION = False
    BASE_URL = "http://localhost:5000"
    CSRF_ENABLED = True
    MONGO_URI = os.environ.get(
        "MONGO_URI", "mongodb://test:test@mongodb:27017/filemanager"
    )


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    PRODUCTION = True

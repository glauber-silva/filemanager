import os

from flask import Flask
from flask_cors import CORS

from app.config import DevelopmentConfig, TestingConfig, ProductionConfig
from app.api import api_v1
from app.api.health.view import healthcheck_bp

def create_app(deploy_env: str = os.getenv("FLASK_ENV", "Development")) -> Flask:
    app = Flask(__name__)
    configuration = {
        "Development": DevelopmentConfig,
        "Testing": TestingConfig,
        "Production": ProductionConfig
    }[deploy_env]

    app.config.from_object(configuration)
    with app.app_context():
        __configure_extensions(app)
    app.app_context().push()

    app.register_blueprint(healthcheck_bp, url_prefix="/api")
    app.register_blueprint(api_v1, url_prefix="/api/v1")

    return app


def __configure_extensions(app: Flask):
    cors = CORS(app, resources={
        r"/*": {
            "origin": "*"
        }
    })
    cors.init_app(app)

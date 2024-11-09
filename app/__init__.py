import os

from flask import Flask
from flask_cors import CORS

from app.config import DevelopmentConfig, TestingConfig, ProductionConfig

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

    @app.route("/hello")
    def hello():
        return "Hello World"

    return app


def __configure_extensions(app: Flask):
    cors = CORS(app, resources={
        r"/*": {
            "origin": "*"
        }
    })
    cors.init_app(app)

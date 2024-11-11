from flask import Blueprint
from flask_restx import Api

from app.api.file.view import ns as file

api_v1 = Blueprint("api", __name__)

api = Api(
    api_v1,
    version="1",
    title="File Manager API",
    description="Application to store and manage files",
    doc="/docs",
)

api.add_namespace(file)

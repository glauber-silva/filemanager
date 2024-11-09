
from http import HTTPStatus

from flask import make_response, jsonify, Blueprint
from flask_restx import Resource, Api



healthcheck_bp = Blueprint('healthcheck', __name__)
api = Api(healthcheck_bp)

@api.route("/healthcheck")
class Health(Resource):


    @api.response(code=200, description="A general check")
    def get(self):
        """
        Check API's health status
        """

        services = {
            "application": "ok"
        }

        return make_response(jsonify({"services": services}), HTTPStatus.OK )
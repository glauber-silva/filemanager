from http import HTTPStatus

from flask import make_response, jsonify
from flask_restx import Resource, Namespace


ns = Namespace("file", "Files Management")

@ns.route("/")
class FileUploadView(Resource):


    @ns.response(code=200, description="Upload a File")
    def post(self):
        """
        Add a file to be stored
        """
        msg = "The file is being processed"
        
        # TODO Add service to upload the File

        return make_response(jsonify({"msg": msg}), HTTPStatus.OK)
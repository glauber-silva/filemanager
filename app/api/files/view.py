from http import HTTPStatus

from flask import make_response, request, jsonify
from flask_restx import Resource, Namespace

from app.api.files.service import TextFileService
from app.api.files.exceptions import FileAlreadyExistsException

ns = Namespace("file", "Files Management")


@ns.route("/")
class FileUploadView(Resource):

    @ns.response(code=200, description="Upload a File")
    def post(self):
        """
        Add a file to be stored
        """
        try:
            service = TextFileService()
            file = request.files['file']
            resp = service.process(file)
            return make_response(jsonify(resp), HTTPStatus.CREATED)
        except FileAlreadyExistsException as e:
            return make_response(jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST)

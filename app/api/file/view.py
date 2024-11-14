import xml.etree.ElementTree as ET

from http import HTTPStatus

from flask import make_response, request, jsonify
from flask_restx import Resource, Namespace

from app.api.file.service import TextFileService
from app.api.file.exceptions import FileAlreadyExistsException, NoFileFoundException

ns = Namespace("file", "Files Management")


@ns.route("/upload")
class FileUploadView(Resource):
    """
    Resource for uploading a new file to the storage.
    """

    @ns.doc("upload_file")
    @ns.response(201, "File uploaded successfully.")
    @ns.response(400, "File already exists or no file found in request.")
    def post(self):
        """
        Upload a file to be stored in GridFS.

        This endpoint allows users to upload files that will be processed and stored in GridFS.
        """
        if "file" not in request.files:
            return make_response(
                jsonify({"error": str(NoFileFoundException())}), HTTPStatus.BAD_REQUEST
            )

        try:
            service = TextFileService()
            file = request.files["file"]
            resp = service.process(file)
        except FileAlreadyExistsException as err:
            return make_response(jsonify({"error": str(err)}), HTTPStatus.BAD_REQUEST)

        return make_response(jsonify(resp), HTTPStatus.CREATED)


@ns.route("/line/random")
class RandomLineView(Resource):
    """
    Resource for retrieving a random line from the stored files.
    """

    @ns.doc("get_random_line")
    @ns.produces(["text/plain", "application/json", "application/xml"])
    @ns.response(200, "Random line retrieved successfully.")
    def get(self):
        """
        Get a random line from the latest file.

        This endpoint returns a random line from the latest uploaded file in text, JSON, or XML format.
        """

        service = TextFileService()
        line_info = service.get_random_line()
        response_type = request.headers.get("Accept", "text/plain")

        if response_type == "application/*":
            return make_response(jsonify(line_info), HTTPStatus.OK)
        if response_type == "application/json":
            return jsonify({"text": line_info["text"]})
        elif response_type == "application/xml":
            line = f"<line><text>{line_info['text']}</text></line>"
            response = make_response(line, HTTPStatus.OK)
            response.mimetype = "application/xml"
            return response

        response = make_response(line_info["text"], HTTPStatus.OK)
        response.headers["Content-Type"] = "text/plain"
        response.mimetype = "text/plain"
        return response


@ns.route("/line/random-backward")
class RandomLineBackwardView(Resource):
    """
    Resource for retrieving a random line from the stored files, reversed.
    """

    @ns.doc("get_random_line_backward")
    @ns.response(200, "Random line retrieved and reversed successfully.")
    def get(self):
        service = TextFileService()
        line = service.get_random_line_backward()
        return make_response(jsonify({"line": line}), HTTPStatus.OK)


@ns.route("/longest")
class FileLineLongestView(Resource):
    """
    Resource for retrieving longest lines from a single file or from multiple.
    """

    @ns.doc("get_longest_lines")
    @ns.response(200, "Longest lines retrieved successfully.")
    def get(self):
        number = int(request.args.get("number", 100))
        service = TextFileService()
        single = request.args.get("single", "false").lower() == "true"

        if single:
            lines = service.get_longest_lines_single_file(number)
        else:
            lines = service.get_longest_lines(number)

        return jsonify(lines)

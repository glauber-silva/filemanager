from http import HTTPStatus

from flask import make_response, request, jsonify
from flask_restx import Resource, Namespace

from app.api.file.service import TextFileService
from app.api.file.exceptions import FileAlreadyExistsException, NoFileFoundException

ns = Namespace("file", "Files Management")


@ns.route("/upload")
class FileUploadView(Resource):

    @ns.response(code=200, description="Upload a File")
    def post(self):
        """
        Add a file to be stored
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

    def get(self):
        service = TextFileService()
        line_info = service.get_random_line()
        response_type = request.headers.get("Accept", "text/plain")

        if response_type == "application/*":
            return make_response(jsonify(line_info), HTTPStatus.OK)
        if response_type == "application/json":
            return jsonify({"text": line_info["text"]})
        elif response_type == "application/xml":
            return (
                f"<line><text>{line_info['text']}</text></line>",
                HTTPStatus.OK,
                {"Content-Type": "application/xml"},
            )

        return line_info["text"], 200, {"Content-Type": "text/plain"}


@ns.route("/line/random-backward")
class RandomLineBackwardView(Resource):

    def get(self):
        service = TextFileService()
        line = service.get_random_line_backward()
        return make_response(jsonify({"line": line}), HTTPStatus.OK)


@ns.route("/longest")
class FileLineLongestView(Resource):

    def get(self):
        number = int(request.args.get("number", 100))
        service = TextFileService()
        single = request.args.get("single", "false").lower() == "true"

        if single:
            lines = service.get_longest_lines_single_file(number)
        else:
            lines = service.get_longest_lines(number)

        return jsonify(lines)

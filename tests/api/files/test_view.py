import unittest
from http import HTTPStatus
from unittest.mock import patch, MagicMock

from flask import Flask
from flask_restx import Api

from app.api.file.view import ns, FileUploadView, RandomLineView, RandomLineBackwardView, FileLineLongestView
from app.api.file.exceptions import FileAlreadyExistsException


class TestFileUploadView(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(ns)
        self.client = self.app.test_client()

    @patch('app.api.file.view.TextFileService')
    def test_post_file_upload_success(self, MockTextFileService):
        mock_service = MockTextFileService.return_value
        mock_service.process.return_value = {"message": "File processed"}

        data = {'file': (MagicMock(), 'test.txt')}
        response = self.client.post('/file/upload', data=data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json, {"message": "File processed"})

    @patch('app.api.file.view.TextFileService')
    def test_post_file_upload_no_file(self, MockTextFileService):
        response = self.client.post('/file/upload')

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("error", response.json)

    @patch('app.api.file.view.TextFileService')
    def test_post_file_upload_file_exists(self, MockTextFileService):
        mock_service = MockTextFileService.return_value
        mock_service.process.side_effect = FileAlreadyExistsException("File already exists")

        data = {'file': (MagicMock(), 'test.txt')}
        response = self.client.post('/file/upload', data=data)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("error", response.json)


class TestRandomLineView(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(ns)
        self.client = self.app.test_client()

    @patch('app.api.file.service.TextFileService')
    def test_get_random_line_plain_text(self, MockTextFileService):
        mock_service = MockTextFileService.return_value
        mock_service.get_random_line.return_value = {"text": "Random line"}

        response = self.client.get('/file/line/random', headers={"Accept": "text/plain"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data.decode(), "Random line")

    @patch('app.api.file.view.TextFileService')
    def test_get_random_line_json(self, MockTextFileService):
        mock_service = MockTextFileService.return_value
        mock_service.get_random_line.return_value = {"text": "Random line"}

        response = self.client.get('/file/line/random', headers={"Accept": "application/json"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, {"text": "Random line"})

    @patch('app.api.file.service.TextFileService')
    def test_get_random_line_xml(self, MockTextFileService):
        mock_service = MockTextFileService.return_value
        mock_service.get_random_line.return_value = {"text": "Random line"}

        response = self.client.get('/file/line/random', headers={"Accept": "application/xml"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data.decode(), "<line><text>Random line</text></line>")


class TestRandomLineBackwardView(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(ns)
        self.client = self.app.test_client()

    @patch('app.api.file.view.TextFileService')
    def test_get_random_line_backward(self, MockTextFileService):
        mock_service = MockTextFileService.return_value
        mock_service.get_random_line_backward.return_value = "Random line backward"

        response = self.client.get('/file/line/random-backward')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, {"line": "Random line backward"})


class TestFileLineLongestView(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(ns)
        self.client = self.app.test_client()

    @patch('app.api.file.view.TextFileService')
    def test_get_longest_lines(self, MockTextFileService):
        mock_service = MockTextFileService.return_value
        mock_service.get_longest_lines.return_value = ["Longest line 1", "Longest line 2"]

        response = self.client.get('/file/longest?number=2')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, ["Longest line 1", "Longest line 2"])

    @patch('app.api.file.view.TextFileService')
    def test_get_longest_lines_single_file(self, MockTextFileService):
        mock_service = MockTextFileService.return_value
        mock_service.get_longest_lines_single_file.return_value = ["Longest line single file"]

        response = self.client.get('/file/longest?number=1&single=true')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, ["Longest line single file"])


if __name__ == '__main__':
    unittest.main()
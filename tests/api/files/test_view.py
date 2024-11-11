import unittest

from app import create_app


class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_random_line(self):
        response = self.app.get("/random_line")
        self.assertIn(response.status_code, [200, 404])

    def test_random_line_backward(self):
        response = self.app.get("/random_line_backward")
        self.assertIn(response.status_code, [200, 404])

    def test_longest_100_lines(self):
        response = self.app.get("/longest_100_lines")
        self.assertIn(response.status_code, [200, 404])

    def test_longest_20_lines_one_file(self):
        response = self.app.get("/longest_20_lines_one_file")
        self.assertIn(response.status_code, [200, 404])

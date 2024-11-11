import hashlib
import random

from bson.objectid import ObjectId

from app.db import mongo, fs
from app.api.file.exceptions import FileAlreadyExistsException


class FileServiceBase:

    def calculate_hash(self, content):
        md5 = hashlib.md5()
        md5.update(content)
        return md5.hexdigest()

    def process(self, file):
        raise NotImplementedError

    def get_file_lines(self):
        raise NotImplementedError

    def get_random_line(self):
        raise NotImplementedError

    def get_random_line_backward():
        raise NotImplementedError

    def get_longest_lines(self, single):
        raise NotImplementedError

    def get_longest_lines_single_file(self):
        raise NotImplementedError


class TextFileService(FileServiceBase):

    def get_file_lines(self, file_id):
        file_data = mongo.db.fs.get(ObjectId(file_id).read().decode("utf-8"))
        return [
            {"text": line, "line_number": i}
            for i, line in enumerate(file_data.splitlines())
        ]

    def get_random_line(self):
        file = random.choice(mongo.db.fs.files.find())
        line = random.choice(self.get_file_lines(file["_id"]))
        line_info = {
            "line": line,
            "line_number": line["line_number"],
            "file_name": file["filename"],
            "most_frequent_letter": get_most_frequent_letter(line["text"]),
        }
        return line_info

    def get_longest_lines(self, number):
        lines = []
        for file in mongo.db.fs.files.find():
            lines += self.get_file_lines(file["_id"])
        lines.sort(key=len, reverse=True)
        return lines[:number]

    def get_random_line_backward(self):
        file = random.choice(mongo.db.fs.files.find())
        line = random.choice(self.get_file_lines(file["_id"]))
        return line[::-1]

    def get_longest_lines_single_file(self, number):
        file = mongo.db.fs.files.find().sort("uploadDate", -1).limit(1)[0]
        lines = self.get_file_lines(file["_id"])
        lines.sort(key=len, reverse=True)
        return lines[:number]

    def process(self, file):

        file_content = file.read()
        file_hash = self.calculate_hash(file_content)

        if mongo.db.files.find_one({"hash": file_hash}):
            raise FileAlreadyExistsException()

        file_id = mongo.save_file(file.filename, file)

        metadata = {
            "filename": file.filename,
            "hash": file_hash,
            "file_id": str(file_id),
        }

        mongo.db.files.insert_one(metadata)

        return metadata

import hashlib
import random
import gridfs
from io import BytesIO
from collections import Counter

from bson.objectid import ObjectId

from app.db import mongo, fs
from app.api.file.exceptions import (
    FileAlreadyExistsException,
    FileNotFound,
    NoContentFound,
)


class FileServiceBase:

    def calculate_hash(self, content):
        md5 = hashlib.md5()
        md5.update(content)
        return md5.hexdigest()

    def get_most_frequent_letter(self, text):
        letters = [char.lower() for char in text if char.isalpha()]
        if not letters:
            return None

        counter = Counter(letters)
        letter, _ = counter.most_common(1)[0]
        return letter

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

    def __init__(self):
        self.fs = gridfs.GridFS(mongo.db)

    def get_file_by_id(self, file_id):
        try:
            file = self.fs.get(ObjectId(file_id))
        except FileNotFound:
            msg = f"No file found with id: {file_id}"
            raise FileNotFound(msg)
        return file

    def get_last_file_metadata(self):
        return mongo.db.files.find().sort("_id", -1).limit(1)[0]

    def get_file_lines(self, file):
        file_data = file.read().decode("utf-8")
        if not file_data:
            raise NoContentFound(
                f"File with id {str(file._id)} is empty or could not be read."
            )
        lines = [
            {"line": i, "text": line} for i, line in enumerate(file_data.splitlines())
        ]
        return lines

    def get_random_line(self):
        last_doc = self.get_last_file_metadata()
        file = self.get_file_by_id(last_doc["file_id"])
        file_lines = self.get_file_lines(file)
        line = random.choice(file_lines)
        line.update(
            {
                "file_name": last_doc["filename"],
                "most_frequent_letter": self.get_most_frequent_letter(line["text"]),
            }
        )
        return line

    def get_longest_lines(self, number):
        lines = []
        for file in mongo.db.fs.files.find():
            lines += self.get_file_lines(file["_id"])
        lines.sort(key=len, reverse=True)
        return lines[:number]

    def get_random_line_backward(self):
        files_count = mongo.db.files.estimated_document_count()
        idx = random.randint(0, files_count - 1)
        file = self.fs.find().skip(idx).next()
        lines = self.get_file_lines(file)
        line = random.choice(lines)
        text = line["text"]
        return text[::-1]

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

        file_id = self.fs.put(BytesIO(file_content), filename=file.filename)

        metadata = {
            "filename": file.filename,
            "hash": file_hash,
            "file_id": str(file_id),
        }

        mongo.db.files.insert_one(metadata.copy())

        return metadata

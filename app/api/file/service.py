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
    """
    Base class for file-related operations. Provides abstract methods for
    common functionalities such as processing files, retrieving lines, and
    identifying frequent letters.
    """

    def calculate_hash(self, content):
        """
        Calculate an MD5 hash of the given file content.
        Args:
            content (bytes): File content in bytes.
        Returns:
            str: MD5 hash of the file content.
        """
        md5 = hashlib.md5()
        md5.update(content)
        return md5.hexdigest()

    def get_most_frequent_letter(self, text):
        """
        Identify the most frequent letter in a text.
        Args:
            text (str): Text content to analyze.
        Returns:
            str or None: The most frequent letter, or None if no letters are found.
        """
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
    """
    Service for handling text files stored in MongoDB via GridFS, providing methods for
    uploading, processing, and retrieving lines from files.
    """

    def __init__(self):
        """
        Initialize the TextFileService with access to GridFS and MongoDB.
        """
        self.fs = gridfs.GridFS(mongo.db)

    def get_file_by_id(self, file_id):
        """
        Retrieve a file by its ObjectId.
        Args:
            file_id (str): ObjectId of the file to retrieve.
        Returns:
            GridOut: The file retrieved from GridFS.

        Raises:
            FileNotFound: If no file is found with the given ID.
        """
        try:
            file = self.fs.get(ObjectId(file_id))
        except FileNotFound:
            msg = f"No file found with id: {file_id}"
            raise FileNotFound(msg)
        return file

    def get_last_file_metadata(self):
        """
        Retrieve metadata for the most recently uploaded file.

        Returns:
            dict: Metadata of the latest file.
        """
        return mongo.db.files.find().sort("_id", -1).limit(1)[0]

    def get_file_lines(self, file):
        """
        Retrieve lines from a file and store them with line numbers.
        Args:
            file (GridOut): The file to read lines from.
        Returns:
            list: A list of dictionaries with line numbers and text content.
        Raises:
            NoContentFound: If the file is empty or cannot be read.
        """
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
        """
        Retrieve a random line from the most recent file.
        Returns:
            dict: A dictionary containing the line text, line number, filename,
                  and most frequent letter.
        """
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
        """
        Retrieve the longest lines from all stored files.
        Args:
            number (int): Number of longest lines to retrieve.
        Returns:
            list: A list of the longest lines across all files.
        """
        lines = []
        for file in mongo.db.fs.files.find():
            lines += self.get_file_lines(file["_id"])
        lines.sort(key=len, reverse=True)
        return lines[:number]

    def get_random_line_backward(self):
        """
        Retrieve a random line from a random file and return it reversed.
        Returns:
            str: A reversed string of the randomly selected line.
        """
        files_count = mongo.db.files.estimated_document_count()
        idx = random.randint(0, files_count - 1)
        file = self.fs.find().skip(idx).next()
        lines = self.get_file_lines(file)
        line = random.choice(lines)
        text = line["text"]
        return text[::-1]

    def get_longest_lines_single_file(self, number):
        """
        Retrieve the longest lines from the most recent file.
        Args:
            number (int): Number of longest lines to retrieve.
        Returns:
            list: A list of the longest lines in the latest file.
        """
        file = mongo.db.fs.files.find().sort("uploadDate", -1).limit(1)[0]
        lines = self.get_file_lines(file["_id"])
        lines.sort(key=len, reverse=True)
        return lines[:number]

    def process(self, file):
        """
        Process a file by calculating its hash and saving it if it does not already exist.
        Args:
            file (FileStorage): The file to be processed and stored.
        Returns:
            dict: Metadata of the stored file, including filename, hash, and file_id.
        Raises:
            FileAlreadyExistsException: If a file with the same hash already exists.
        """

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

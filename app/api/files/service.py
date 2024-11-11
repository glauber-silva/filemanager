import hashlib

from typing import Any
from app.db import mongo
from app.api.files.exceptions import FileAlreadyExistsException

class FileServiceBase:

    def calculate_hash(self, content):
        md5 = hashlib.md5()
        md5.update(content)
        return md5.hexdigest()

    def process(self, file) -> Any:
        raise NotImplementedError
    



class TextFileService(FileServiceBase):


    def process(self, file):

        # files_collection = mongo.db.files
        
        file_content = file.read()
        file_hash = self.calculate_hash(file_content)

        if mongo.db.files.find_one({"hash": file_hash}):
            return FileAlreadyExistsException()
        
        file_id = mongo.save_file(file_content, filename=file.filename)

        metadata = {
            "filename": file.filename,
            "hash": file_hash,
            "file_id": file_id
        }

        mongo.db.files.insert_one(metadata)

        return metadata
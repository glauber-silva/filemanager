class FileAlreadyExistsException(Exception):
    def __init__(self, message="Duplicate file detected"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class NoFileFoundException(Exception):
    def __init__(self, message="Your request is missing the file to upload."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

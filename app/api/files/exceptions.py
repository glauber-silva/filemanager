class FileAlreadyExistsException(Exception):
    def __init__(self, message="Duplicate file detected"):
        self.message = message
        super().__init__(self.message)
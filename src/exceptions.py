class FileTypeExtractionError(Exception):
    def __init__(self, file_path):
        self.file_path = file_path
        super().__init__(
            "FileTypeExtractionError: "
            f"Unable to get file extension from {file_path}"
        )

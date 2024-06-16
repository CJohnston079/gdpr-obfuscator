class FileTypeExtractionError(Exception):
    def __init__(self, file_path):
        self.file_path = file_path
        super().__init__(
            "FileTypeExtractionError: "
            f"unable to get file extension from {file_path}"
        )


class UnsupportedFile(Exception):
    def __init__(self, file_type):
        self.file_type = file_type
        super().__init__(
            "UnsupportedFile: " f"file type .{file_type} is not supported."
        )

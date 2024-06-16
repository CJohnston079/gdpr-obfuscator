import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class GetDataError(Exception):
    def __init__(self, file_path, e):
        self.file_path = file_path
        self.e = e
        super().__init__(
            f"GetDataError: error fetching data from {file_path}: {e}\n\n"
        )
        logger.error(self.__str__(), exc_info=True)


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

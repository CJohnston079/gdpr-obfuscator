import logging

from src.exceptions import FileTypeExtractionError
from src.exceptions import GetDataError
from src.exceptions import UnsupportedFile
from src.utils.get_data import get_data
from src.utils.obfuscate_fields import obfuscate_fields
from src.utils.serialise_dicts import serialise_dicts


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def obfuscator(event):
    try:
        file_path = event["file_to_obfuscate"]
        fields_to_obfuscate = event["pii_fields"]

        data = get_data(file_path)
        obfuscated_data = obfuscate_fields(data, fields_to_obfuscate)
        serialized_data = serialise_dicts(obfuscated_data)

        return serialized_data

    except (FileTypeExtractionError, UnsupportedFile) as e:
        raise GetDataError(file_path, e)
    except Exception as e:
        logger.critical("An unexpected error occurred", exc_info=True)
        raise e

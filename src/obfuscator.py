import logging

from botocore.exceptions import ClientError

from src.exceptions import GetDataError
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

    except (GetDataError, ClientError, TypeError) as e:
        logger.error(
            f"Error loading data from {file_path}: {e}", exc_info=True
        )
        raise e
    except Exception as e:
        logger.critical("An unexpected error occurred", exc_info=True)
        raise e

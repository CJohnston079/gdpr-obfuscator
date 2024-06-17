import logging

from botocore.exceptions import ClientError

from src.exceptions import FormatDataError
from src.exceptions import GetDataError
from src.exceptions import ObfuscationError
from src.utils.format_data import format_data
from src.utils.get_data import get_data
from src.utils.obfuscate_fields import obfuscate_fields


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def obfuscator(event):
    try:
        file_path = event["file_to_obfuscate"]
        fields_to_obfuscate = event["pii_fields"]

        data = get_data(file_path)
        obfuscated_data = obfuscate_fields(data, fields_to_obfuscate)
        formatted_data = format_data(obfuscated_data)

        return formatted_data

    except (GetDataError, ClientError, TypeError) as e:
        logger.error(
            f"Error loading data from {file_path}: {e}", exc_info=True
        )
        raise e
    except ObfuscationError as e:
        logger.error(f"Error obfuscating fields: {e}", exc_info=True)
        raise e
    except FormatDataError as e:
        logger.error(f"Error formatting obfuscated data: {e}", exc_info=True)
        raise e
    except Exception as e:
        logger.critical("An unexpected error occurred", exc_info=True)
        raise e

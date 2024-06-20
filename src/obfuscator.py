import logging

from botocore.exceptions import ClientError

from src.exceptions import FormatDataError
from src.exceptions import GetDataError
from src.exceptions import ObfuscationError
from src.utils.format_data import format_data
from src.utils.get_data import get_data
from src.utils.get_file_type import get_file_type
from src.utils.obfuscate_fields import obfuscate_fields
from src.utils.obfuscation_methods.tokenise import tokenise


class Obfuscator:
    def __init__(self, log_level=logging.DEBUG, method=tokenise, **options):
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(__name__)
        self.log_error = lambda msg, *args, **kwargs: (
            self.logger.error(msg, exc_info=True, *args, **kwargs)
        )
        self.obfuscation_method = method
        self.method_options = options.get("options", {})

    def obfuscate(self, event):
        """
        Obfuscates personally identifiable information (PII) fields in a data
        file located in an AWS S3 bucket.

        Args:
            event (dict): A dictionary containing the following keys:
                file_to_obfuscate (str): The AWS S3 URI of the file to be
                    obfuscated.
                pii_fields (list): A list of strings of PII fields to be
                    obfuscated.

        Returns:
            str: The obfuscated data in the same format as the input file.

        Raises:
            AttributeError: If there is an error extracting the file type.
            GetDataError: If there is an error loading the data from the file.
            ClientError: If there is an AWS error loading the data.
            TypeError: If there the file type is not supported.
            ObfuscationError: If there is an error obfuscating the PII fields.
            FormatDataError: If there is an error formatting the data.
            Exception (critical): If an unexpected error occurs.
        """
        try:
            file_path = event["file_to_obfuscate"]
            file_type = get_file_type(file_path)
            obfuscation_options = {
                "pii_fields": event["pii_fields"],
                "obfuscation_method": self.obfuscation_method,
                "options": self.method_options,
            }

            data = get_data(file_path, file_type)
            obfuscated_data = obfuscate_fields(data, obfuscation_options)
            formatted_data = format_data(obfuscated_data, file_type)

            return formatted_data

        except AttributeError as e:
            self.log_error(f"Error extracting file type: {e}")
            raise e
        except (GetDataError, ClientError, TypeError) as e:
            self.log_error(f"Error loading data from {file_path}: {e}")
            raise e
        except ObfuscationError as e:
            self.log_error(f"Error obfuscating fields: {e}")
            raise e
        except FormatDataError as e:
            self.log_error(f"Error formatting obfuscated data: {e}")
            raise e
        except Exception as e:
            self.logger.critical("An unexpected error occurred", exc_info=True)
            raise e

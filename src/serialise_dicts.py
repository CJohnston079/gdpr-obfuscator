import io
import pickle


def serialise_dicts(dicts):
    """
    Serialize a list of dictionaries using pickle.

    Args:
        dicts (list of dict): A list of dictionaries to be serialized.

    Returns:
        bytes: The serialized data representing the input list of dictionaries.
    """
    buffer = io.BytesIO()

    pickle.dump(dicts, buffer)
    buffer.seek(0)
    serialised_data = buffer.getvalue()

    return serialised_data

import io
import pickle


def serialise_dicts(dicts):
    buffer = io.BytesIO()

    pickle.dump(dicts, buffer)
    buffer.seek(0)
    serialised_data = buffer.getvalue()

    return serialised_data

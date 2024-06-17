import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def format_parquet_data(data):
    """
    Formats a data structure into a Parquet string ready for writing.

    Args:
        data (str): The data to be formatted

    Returns:
        str: A Parquet formatted string.
    """
    if data == []:
        return b""

    table = pa.Table.from_pandas(pd.DataFrame(data))
    output = pa.BufferOutputStream()
    pq.write_table(table, output)
    serialized_parquet = output.getvalue()

    return serialized_parquet

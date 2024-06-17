import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def format_parquet_data(data):
    if data == []:
        return b""

    table = pa.Table.from_pandas(pd.DataFrame(data))
    output = pa.BufferOutputStream()
    pq.write_table(table, output)
    serialized_parquet = output.getvalue()

    return serialized_parquet

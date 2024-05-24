def obfuscate_fields(data, fields):
    return [
        {key: '***' if key in fields else value for key, value in record.items()}
        for record in data
    ]

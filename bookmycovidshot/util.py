def is_empty(data, field):
    if field not in data:
        return True
    value = data[field]
    if isinstance(value, (str, bytes)):
        if value.strip():
            return False
        return True
    return bool(value)

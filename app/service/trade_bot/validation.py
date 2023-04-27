import re


def validate_phone(value: str) -> str:
    value = value.strip()
    try:
        pattern = re.compile("[0-9]*")
        if not pattern.match(value):
            raise RuntimeError("Wrong format.")
        if len(value) != 11:
            raise RuntimeError("Wrong format.")
    except Exception:
        raise RuntimeError("Wrong format.")
    return value

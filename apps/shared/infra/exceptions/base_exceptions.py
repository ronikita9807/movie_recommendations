class ObjectExistsException(Exception):
    def __init__(self, message: str):
        self._message = message

    def __str__(self) -> str:
        return f"Object already exists, details: {self._message}"

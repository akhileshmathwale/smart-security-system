class DatabaseException(Exception):
    def __init__(self, key):
        super().__init__(f"Database file missing or no data found for the given key :: {key}")


class CameraOpeningError(Exception):
    def __init__(self, id):
        super().__init__(f"Error opening camera, incorrect camera id :: {id}")

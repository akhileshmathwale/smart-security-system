import os
import pickle

from ..constant import DB_FILE
from ..exception import DatabaseException


class DataStore:
    @staticmethod
    def load(protocol="rb"):
        return open(DB_FILE, protocol)

    @staticmethod
    def write(val):
        key = 0  # default key

        if os.path.isfile(DB_FILE):
            data = pickle.load(file=DataStore.load())
            key = len(data)
            data[key] = val
        else:
            data = {0: str(val)}

        pickle.dump(data, file=DataStore.load("wb"))
        return key

    @staticmethod
    def read(key):
        val = pickle.load(DataStore.load())
        if isinstance(val, dict) and key in val:
            return val[key]
        else:
            raise DatabaseException(key)

from enum import Enum

class ExeBatchType(Enum):
    """ バッチ区分列挙型
    """

    NEW_FILE_CREATE_BATCH = 1
    ERROR_FILE_CREATE_BATCH = 2
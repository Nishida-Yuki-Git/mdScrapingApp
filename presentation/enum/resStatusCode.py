from enum import Enum

class ResStatusCode():
    def __init__(self):
        self.success_code = 0
        self.error_code = 1

    def getSuccessCode(self):
        return self.success_code
    def getErrorCode(self):
        return self.error_code
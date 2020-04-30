"""A module containing all custom errors related to datascraping"""

class DataCollectionError(Exception):
    """Base class for all DataCollectionTools Errors"""
    pass

class ServerError(DataCollectionError):
    """Exception raised when server sends undesirable response

    Attributes:
        response_code: the response code warranting an error
        message: explanation of error
    """

    def __init__(self, response_code, message):
        self.response_code = response_code
        self.message = message

class ForbiddenError(DataCollectionError):
    """Exception raised when server bans you. (Response code 403)

    Attributes:
        response_code: the response code warranting an error
        message: explanation of error
    """

    def __init__(self, message, response_code=403):
        self.response_code = response_code
        self.message = message


class ThrottleError(DataCollectionError):
    """Exception raised when webserver throttles access to docs

    Attributes:
        message: explanation of error
    """

    def __init__(self, message):
        self.message = message

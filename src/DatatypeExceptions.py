"""A module containing all custom errors related to datatype initialization and modification."""

class CardOccuranceError(Exception):
    """Base class for all CardOccurance Errors"""
    pass

class DatePricingExcption(CardOccuranceError):
    """Exception raised when Card

    Attributes:
        message: explanation of error
    """

    def __init__(self, message):
        self.message = message

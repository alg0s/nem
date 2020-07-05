# author: goodalg0s@gmail.com

class BaseError(Exception):
    ''' A base error for custom errors '''

    def __init__(self, message):
        self.message = message
        print(self.message)

    def __str__(self):
        return repr(self.message)


class FieldParseError(BaseError):
    ''' Raised when an error occurs during field value parsing '''


class RowParseError(BaseError):
    ''' Raised when an error occurs during row parsing '''


class InvalidRowError(BaseError):
    ''' Raised when a row is invalid based on AEMO definition '''

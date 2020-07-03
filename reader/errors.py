# author: goodalg0s@gmail.com

class BaseError(Exception):
    ''' A base error for custom errors '''

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


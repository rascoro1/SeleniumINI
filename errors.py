
class NotValidAttributeException(Exception):
    def __init__(self, message, errors):
            super(NotValidAttributeException, self).__init__(message)
            self.errors = errors

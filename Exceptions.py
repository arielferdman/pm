class LandPageException(Exception):
    """
    base class for landing page exceptions.
    """
    def __init__(self, message=None):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message


class JsonValidationError(LandPageException):
    """
    general Exception for invalid json files, specific details in the message.
    require a message argument.
    """
    def __init__(self, message):
        super().__init__()
        self.message = message


class EmailDuplicationError(LandPageException):
    """
    email duplication error have a default message.
    """
    def __init__(self, message="This email address already exists in the database."):
        super().__init__()
        self.message = message

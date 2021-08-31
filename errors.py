class LandPageError(Exception):
    """
    base class for landing page exceptions.
    """
    def __init__(self, expression, message):
        super().__init__()
        self.message = message
        self.expression = expression

    def __str__(self):
        return f"{self.message}\t{self.expression}"


class JsonValidationError(LandPageError):
    """
    general Exception for invalid json files, specific details in the message.
    require a message argument.
    """
    def __init__(self, expression, message):
        super().__init__(expression, message)


class EmailDuplicationError(LandPageError):
    """
    email duplication error have a default message.
    """
    def __init__(self, expression, message):
        super().__init__(expression, message)



class Error(Exception):
    pass


class InvalidInput(Error):
    """ raised when user's isn't a number between 0-11"""
    pass


class EmptyPit(Error):
    """ raised when user's choice is an empty pit"""
    pass

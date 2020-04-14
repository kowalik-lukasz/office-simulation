# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class ObjectOutOfAcceptedXBoundsError(Error):
    """Raised when the position of blitted object does not match the expected resolution"""
    pass


class ObjectOutOfAcceptedYBoundsError(Error):
    """Raised when the position of blitted object does not match the expected resolution"""
    pass

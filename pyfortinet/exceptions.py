"""FMG API exceptions"""


class FMGException(Exception):
    """General FMG error"""


class FMGTokenException(FMGException):
    """No Token error"""


class FMGAuthenticationException(FMGException):
    """Authentication error"""


class FMGLockNeededException(FMGException):
    """Lock needed error"""


class FMGLockException(FMGException):
    """Locking error"""


class FMGWrongRequestException(FMGException):
    """Locking error"""


class FMGUnhandledException(FMGException):
    """Unhandled error"""


class FMGEmptyResultException(FMGException):
    """No result for a request"""


class FMGInvalidDataException(FMGException):
    """The data is invalid for selected url"""


class FMGObjectAlreadyExistsException(FMGException):
    """The object is already in the database"""


class FMGMissingScopeException(FMGException):
    """Scope must be set before referencing URL"""

"""FMG API exceptions"""


class FMGException(Exception):
    """General FMG error"""


class FMGConfigurationException(FMGException):
    """FMG configuration problem"""


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


class FMGObjectNotExistException(FMGException):
    """Object does not exist"""


class FMGInvalidDataException(FMGException):
    """The data is invalid for selected url"""


class FMGObjectAlreadyExistsException(FMGException):
    """The object is already in the database"""


class FMGMissingScopeException(FMGException):
    """Scope must be set before referencing URL"""


class FMGInvalidURL(FMGException):
    """Invalid URL"""


class FMGNotAssignedException(FMGException):
    """FMG not assigned to object"""


class FMGMissingMasterKeyException(FMGException):
    """Master key is missing for this API class"""

class FMGDataSrcDuplicateException(FMGException):
    """Duplicate name found in data namespace"""

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


class FMGHTTPException(FMGException):
    """An HTTP error prevented FortiManager from returning a JSON-RPC result."""

    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(f"FortiManager HTTP request failed with status {status_code}")


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

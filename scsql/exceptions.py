class Warning(Exception):
    """Base class for warnings"""

class Error(Exception):
    """Base class for errors"""

class InterfaceError(Error):
    """Exception raised for errors in the database interface"""

class DatabaseError(Error):
    """Exception raised for errors in the database itself"""

class DataError(DatabaseError):
    """Exception raised for errors in the processed data"""

class OperationalError(DatabaseError):
    """Exception raised for errors that are likely to be corrected by restarting
    the transaction"""

class IntegrityError(DatabaseError):
    """Exception raised when the database integrity is compromised"""

class InternalError(DatabaseError):
    """Exception raised when the database encounters an internal error"""

class ProgrammingError(DatabaseError):
    """Exception raised for programming errors"""

class NotSupportedError(DatabaseError):
    """Exception raised in case a method is not supported"""

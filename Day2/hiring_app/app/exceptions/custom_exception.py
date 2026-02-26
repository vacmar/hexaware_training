class HiringAppException(Exception):
    """Base exception for Hiring Application"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class UserNotFoundException(HiringAppException):
    """Exception raised when a user is not found"""
    def __init__(self, user_id: int = None):
        message = f"User with ID {user_id} not found" if user_id else "User not found"
        super().__init__(message)

class JobNotFoundException(HiringAppException):
    """Exception raised when a job is not found"""
    def __init__(self, job_id: int = None):
        message = f"Job with ID {job_id} not found" if job_id else "Job not found"
        super().__init__(message)

class ApplicationNotFoundException(HiringAppException):
    """Exception raised when an application is not found"""
    def __init__(self, application_id: int = None):
        message = f"Application with ID {application_id} not found" if application_id else "Application not found"
        super().__init__(message)

class DuplicateEmailException(HiringAppException):
    """Exception raised when attempting to register a duplicate email"""
    def __init__(self, email: str = None):
        message = f"Email {email} is already registered" if email else "Email already registered"
        super().__init__(message)

class DuplicateApplicationException(HiringAppException):
    """Exception raised when a user tries to apply for the same job twice"""
    def __init__(self):
        super().__init__("User has already applied for this job")

class InvalidStatusTransitionException(HiringAppException):
    """Exception raised when an invalid status transition is attempted"""
    def __init__(self, from_status: str, to_status: str):
        message = f"Cannot transition from {from_status} to {to_status}"
        super().__init__(message)

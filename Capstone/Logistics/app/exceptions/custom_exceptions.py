"""
Custom exceptions for the application
"""
from typing import Any


class LogisticsBaseException(Exception):
    """Base exception for the logistics application"""
    
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class EmailAlreadyExistsException(LogisticsBaseException):
    """Exception raised when email already exists"""
    
    def __init__(self, email: str):
        super().__init__(
            message=f"User with email '{email}' already exists",
            status_code=409
        )


class InvalidCredentialsException(LogisticsBaseException):
    """Exception raised for invalid login credentials"""
    
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message=message, status_code=401)


class UserNotFoundException(LogisticsBaseException):
    """Exception raised when user is not found"""
    
    def __init__(self, user_id: Any):
        super().__init__(
            message=f"User with ID '{user_id}' not found",
            status_code=404
        )


class ShipmentNotFoundException(LogisticsBaseException):
    """Exception raised when shipment is not found"""
    
    def __init__(self, identifier: Any):
        super().__init__(
            message=f"Shipment '{identifier}' not found",
            status_code=404
        )


class ShipmentCannotBeCancelledException(LogisticsBaseException):
    """Exception raised when shipment cannot be cancelled"""
    
    def __init__(self, tracking_number: str):
        super().__init__(
            message=f"Shipment '{tracking_number}' cannot be cancelled after dispatch",
            status_code=400
        )


class HubNotFoundException(LogisticsBaseException):
    """Exception raised when hub is not found"""
    
    def __init__(self, hub_id: Any):
        super().__init__(
            message=f"Hub with ID '{hub_id}' not found",
            status_code=404
        )


class HubAlreadyExistsException(LogisticsBaseException):
    """Exception raised when hub with same name already exists"""
    
    def __init__(self, hub_name: str):
        super().__init__(
            message=f"Hub with name '{hub_name}' already exists",
            status_code=409
        )


class AgentNotFoundException(LogisticsBaseException):
    """Exception raised when agent is not found"""
    
    def __init__(self, agent_id: Any):
        super().__init__(
            message=f"Agent with ID '{agent_id}' not found",
            status_code=404
        )


class UnauthorizedAccessException(LogisticsBaseException):
    """Exception raised for unauthorized access"""
    
    def __init__(self, message: str = "You are not authorized to perform this action"):
        super().__init__(message=message, status_code=403)

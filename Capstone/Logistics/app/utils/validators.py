"""
Validation utilities
"""
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """Validate email format"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Allow various formats: +1234567890, 123-456-7890, (123) 456-7890
    phone_pattern = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]*$'
    return bool(re.match(phone_pattern, phone)) and len(re.sub(r'\D', '', phone)) >= 10


def validate_tracking_number(tracking_number: str) -> bool:
    """Validate tracking number format"""
    # Format: TRK followed by 10 alphanumeric characters
    pattern = r'^TRK[A-Z0-9]{10}$'
    return bool(re.match(pattern, tracking_number))


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength.
    
    Returns tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, None


def sanitize_string(value: str) -> str:
    """Sanitize string input"""
    # Remove leading/trailing whitespace
    value = value.strip()
    # Remove multiple spaces
    value = re.sub(r'\s+', ' ', value)
    return value

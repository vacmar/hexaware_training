from fastapi import HTTPException


class UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")


class InvalidLoanAmountError(HTTPException):
    def __init__(self, message: str = "Invalid loan amount"):
        super().__init__(status_code=400, detail=message)


class LoanApplicationError(HTTPException):
    def __init__(self, message: str = "Error processing loan application"):
        super().__init__(status_code=400, detail=message)


class UnauthorizedError(HTTPException):
    def __init__(self, message: str = "Unauthorized action"):
        super().__init__(status_code=403, detail=message)

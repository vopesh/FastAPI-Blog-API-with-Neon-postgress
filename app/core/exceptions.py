from pydantic import BaseModel
from fastapi import HTTPException
from typing import Optional

class ErrorResponse(BaseModel):
    message: str
    error_type: str
    details: Optional[dict] = None

class AppException(HTTPException):
    def __init__(self, status_code: int, message: str, error_type: str, details: Optional[dict] = None):
        self.error_response = ErrorResponse(
            message=message, error_type=error_type, details=details)
        super().__init__(status_code=status_code, detail=self.error_response.model_dump())

class ValidationException(AppException):
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(status_code=422, message=message, error_type="validation_error", details=details)

class UnauthorizedException(AppException):
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(status_code=401, message=message, error_type="unauthorized_error", details=details)

class BadRequestException(AppException):
    def __init__(self, message: str):
        super().__init__(status_code=400, message=message, error_type="bad_request_error")

class InternalServerErrorException(AppException):
    def __init__(self, message: str):
        super().__init__(status_code=500, message=message, error_type="internal_server_error")

class NotFoundException(AppException):
    def __init__(self, message: str):
        super().__init__(status_code=404, message=message, error_type="not_found_error")

class ForbiddenException(AppException):
    def __init__(self, message: str):
        super().__init__(status_code=403, message=message, error_type="forbidden_error")

class ConflictException(AppException):
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(status_code=409, message=message, error_type="conflict_error", details=details)

class AuthenticationException(AppException):
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(status_code=401, message=message, error_type="authentication_error", details=details)

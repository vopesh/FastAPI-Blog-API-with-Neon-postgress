import re
from app.core.exceptions import ValidationException
    
class PasswordValidators:
    @staticmethod
    def validate(password: str) -> bool:
        if len(password) < 8:
            raise ValidationException("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            raise ValidationException("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            raise ValidationException("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', password):
            raise ValidationException("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]', password):
            raise ValidationException("Password must contain at least one special character")
        return True

    @staticmethod
    def validate_password(password: str) -> bool:
        return PasswordValidators.validate(password)
    
class EmailValidators:
    @staticmethod
    def validate(email: str) -> bool:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValidationException("Invalid email format")
        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        return EmailValidators.validate(email)

class StringValidators:
    @staticmethod
    def validate_non_empty(value: str, field_name: str) -> None: 
        if not value or value.strip() == "":
            raise ValidationException(f"{field_name} cannot be empty.")
    
    @staticmethod    
    def validate_max_length(value: str, field_name: str, min_lenghth: int=3, max_length: int=255) -> None:
        if len(value) > max_length and len(value) < min_lenghth:
            raise ValidationException(f"{field_name} cannot exceed {max_length} characters.")



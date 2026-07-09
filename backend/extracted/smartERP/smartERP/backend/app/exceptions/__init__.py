"""Custom business exceptions for SmartERP.

These exceptions are raised by the service layer when business rules
are violated. They are distinct from HTTP exceptions and should be
caught and converted to appropriate HTTP responses in the API layer.
"""


class BusinessRuleError(Exception):
    """Base exception for business rule violations."""

    pass


class DuplicateCompanyCodeError(BusinessRuleError):
    """Raised when attempting to create or update with a duplicate company code."""

    pass


class DuplicateGSTError(BusinessRuleError):
    """Raised when attempting to create or update with a duplicate GST number."""

    pass


class CompanyNotFoundError(BusinessRuleError):
    """Raised when a company cannot be found by the provided identifier."""

    pass


class InvalidCompanyDataError(BusinessRuleError):
    """Raised when company data fails business validation."""

    pass


class DuplicateUsernameError(BusinessRuleError):
    """Raised when attempting to create or update with a duplicate username."""

    pass


class DuplicateEmailError(BusinessRuleError):
    """Raised when attempting to create or update with a duplicate email."""

    pass


class DuplicateEmployeeCodeError(BusinessRuleError):
    """Raised when attempting to create or update with a duplicate employee code."""

    pass


class UserNotFoundError(BusinessRuleError):
    """Raised when a user cannot be found by the provided identifier."""

    pass


class InvalidCredentialsError(BusinessRuleError):
    """Raised when authentication credentials are invalid."""

    pass


class AccountInactiveError(BusinessRuleError):
    """Raised when attempting to authenticate with an inactive account."""

    pass


class AccountLockedError(BusinessRuleError):
    """Raised when attempting to authenticate with a locked account."""

    pass


class InvalidPasswordError(BusinessRuleError):
    """Raised when the provided password is incorrect."""

    pass


class AppException(Exception):
  def __init__(self, message: str, error_code: str, status_code: int = 400):
    self.message = message
    self.error_code = error_code
    self.status_code = status_code

class NotFoundError(AppException):
  def __init__(self, resource: str, identifier: str | int):
    super().__init__(
      message=f"{resource} with id {str(identifier)} not found",
      error_code="RESOURCE_NOT_FOUND",
      status_code=404
    )

class ValidationError(AppException):
  def __init__(self, message: str):
    super().__init__(
      message=message,
      error_code="VALIDATION_ERROR",
      status_code=400
    )

class ConflictError(AppException):
  def __init__(self, message):
    super().__init__(
      message=message,
      error_code="CONFLICT",
      status_code=409
    )
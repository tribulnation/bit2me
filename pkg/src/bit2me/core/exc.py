from typing_extensions import Any

class Error(Exception):
  def __str__(self):
    args = self.args[0] if len(self.args) == 1 else ', '.join(self.args)
    return f'{self.__class__.__name__}({args})'

class NetworkError(Error):
  """Error accessing the API"""
  def __str__(self):
    return super().__str__()

class ValidationError(Error):
  """The response shape did not match the expected schema"""
  def __str__(self):
    return super().__str__()

class ApiError(Error):
  """The remote API returned a non 2xx status code"""
  def __init__(self, status: int, payload: Any, *args):
    self.status = status
    self.payload = payload
    super().__init__(status, payload, *args)

  def __str__(self):
    return f'ApiError({self.status}), {self.payload})'

  @staticmethod
  def of(status: int, payload: Any, *args):
    if status == 400:
      cls = BadRequest
    elif status == 401:
      cls = Unauthorized
    elif status == 404:
      cls = NotFound
    elif status == 429:
      cls = RateLimited
    elif status == 404:
      cls = NotFound
    elif 500 <= status < 600:
      cls = InternalServerError
    else:
      cls = ApiError
    return cls(status, payload, *args)

class RateLimited(ApiError):
  """The remote API returned a 429 status code"""
  def __str__(self):
    return super().__str__()

class BadRequest(ApiError):
  """The remote API returned a 400 status code"""
  def __str__(self):
    return super().__str__()

class Unauthorized(ApiError):
  """The remote API returned a 401 status code"""
  def __str__(self):
    return super().__str__()

class NotFound(ApiError):
  """The remote API returned a 404 status code"""
  def __str__(self):
    return super().__str__()

class InternalServerError(ApiError):
  """The remote API returned a 5xx status code"""
  def __str__(self):
    return super().__str__()
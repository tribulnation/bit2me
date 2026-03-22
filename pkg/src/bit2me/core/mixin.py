from typing_extensions import TypeVar, Any
import os
from dataclasses import dataclass
import httpx

from .http import HttpMixin, AuthHttpMixin, AuthHttpClient, BIT2ME_API_URL
from .exc import ApiError

T = TypeVar('T')

@dataclass(kw_only=True)
class Endpoint(HttpMixin):
  default_validate: bool = True

  def should_validate(self, validate_param: bool | None = None) -> bool:
    return self.default_validate if validate_param is None else validate_param

  def raise_error(self, response: httpx.Response):
    try:
      payload: Any = response.json()
    except:
      payload = response.text
    raise ApiError.of(response.status_code, payload)

@dataclass
class AuthEndpoint(Endpoint, AuthHttpMixin):

  @classmethod
  def new(
    cls, api_key: str | None = None, api_secret: str | None = None, *,
    base_url: str = BIT2ME_API_URL, validate: bool = True,
  ):
    if api_key is None:
      api_key = os.environ['BIT2ME_API_KEY']
    if api_secret is None:
      api_secret = os.environ['BIT2ME_SECRET_KEY']
    client = AuthHttpClient(api_key=api_key, api_secret=api_secret)
    return cls(base_url=base_url, http=client, default_validate=validate)

  @classmethod
  def public(cls, *, base_url: str = BIT2ME_API_URL, validate: bool = True):
    return cls.new('', '', base_url=base_url, validate=validate)

@dataclass
class Router(Endpoint):
  def __post_init__(self):
    for field, cls in self.__annotations__.items():
      if issubclass(cls, Endpoint) or issubclass(cls, Router):
        setattr(self, field, cls(base_url=self.base_url, http=self.http, default_validate=self.default_validate))

@dataclass
class AuthRouter(Router, AuthEndpoint):
  ...

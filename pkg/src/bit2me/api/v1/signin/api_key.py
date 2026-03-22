from typing_extensions import NotRequired, TypedDict
from bit2me.types import TokenResponse
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class SignInApiKeyRequest(TypedDict):
  userId: NotRequired[str]

class SignInApiKeyResponse(TypedDict):
  accessToken: TokenResponse

adapter = TypeAdapter(SignInApiKeyResponse)

class ApiKey(Endpoint):
  async def api_key(
    self,
    sign_in_api_key_request: SignInApiKeyRequest,
    *,
    validate: bool = True
  ) -> SignInApiKeyResponse:
    """Authorize a user with an API key.
    
    - `sign_in_api_key_request`: Sign-in payload
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/access/POST/v1/signin/apikey)"""
    r = await self.authed_request(
      'POST', '/v1/signin/apikey',
      json=sign_in_api_key_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

from typing_extensions import NotRequired, TypedDict
from bit2me.types import TokenResponse
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class Session(TypedDict):
  id: str
  expirationTime: int

class SignInEmbedRequest(TypedDict):
  accessToken: str

class SignInEmbedResponse(TypedDict):
  accessToken: TokenResponse
  refreshToken: TokenResponse
  session: NotRequired[Session]

adapter = TypeAdapter(SignInEmbedResponse)

class Embed(Endpoint):
  async def embed(
    self,
    sign_in_embed_request: SignInEmbedRequest,
    *,
    validate: bool = True
  ) -> SignInEmbedResponse:
    """Generate access and refresh tokens for the embed session and subsequent API calls.
    
    - `sign_in_embed_request`: Sign-in payload
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/access/POST/v1/signin/embed)"""
    r = await self.request('POST', '/v1/signin/embed', json=sign_in_embed_request)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

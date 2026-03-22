from typing_extensions import Literal, NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class SignInTwoFactorV3response(TypedDict):
  sfaType: Literal['gauth', 'email', 'sms', 'call', 'whatsapp']
  retryIntervalSeconds: NotRequired[float]

adapter = TypeAdapter(SignInTwoFactorV3response)

class TwoFactor(Endpoint):
  async def two_factor(self, *, validate: bool = True) -> SignInTwoFactorV3response:
    """Get the active user verification method and initialize the verification process.
    
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/access/GET/v3/signin/sfa)"""
    r = await self.authed_request('GET', '/v3/signin/sfa')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

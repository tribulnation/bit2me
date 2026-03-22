from bit2me.types import BooleanResultResponse
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

adapter = TypeAdapter(BooleanResultResponse)

class Ibans(AuthEndpoint):
  async def __call__(self, *, iban: str, validate: bool = True) -> BooleanResultResponse:
    """Check whether an IBAN is valid.
    
    - `iban`: Iban to check
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/funding/GET/v1/teller/iban/validate)"""
    params: dict = {
      'iban': iban,
    }
    r = await self.authed_request('GET', '/v1/teller/iban/validate', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

from bit2me.types import BooleanResultResponse
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

adapter = TypeAdapter(BooleanResultResponse)

class Submit(AuthEndpoint):
  async def submit(self, *, validate: bool = True) -> BooleanResultResponse:
    """Send the data to be verified (change the status to pending)
    
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/POST/v1/account/verify/identity)"""
    r = await self.authed_request('POST', '/v1/account/verify/identity')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

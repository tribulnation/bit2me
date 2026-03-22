from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

adapter = TypeAdapter(None)

class Delete(AuthEndpoint):
  async def __call__(self, *, validate: bool = True) -> None:
    """Delete user account
    
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/DELETE/v1/account)"""
    r = await self.authed_request('DELETE', '/v1/account')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

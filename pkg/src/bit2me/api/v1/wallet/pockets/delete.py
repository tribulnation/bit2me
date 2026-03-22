from bit2me.types import BooleanResultResponse
from pydantic import TypeAdapter
from bit2me.core import Endpoint

adapter = TypeAdapter(BooleanResultResponse)

class Delete(Endpoint):
  async def delete(self, *, id: str, validate: bool = True) -> BooleanResultResponse:
    """Delete a pocket
    
    - `id`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/wallet/DELETE/v1/wallet/pocket)"""
    params: dict = {
      'id': id,
    }
    r = await self.authed_request('DELETE', '/v1/wallet/pocket', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

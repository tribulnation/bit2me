from bit2me.types import PayOrderData
from pydantic import TypeAdapter
from bit2me.core import Endpoint

adapter = TypeAdapter(list[PayOrderData])

class List(Endpoint):
  async def list(self, *, validate: bool = True) -> list[PayOrderData]:
    """Get all pending pay order of a user
    
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/transfers/GET/v1/social-pay/order)"""
    r = await self.authed_request('GET', '/v1/social-pay/order')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

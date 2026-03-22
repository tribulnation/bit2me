from bit2me.types import OrderResponse
from pydantic import TypeAdapter
from bit2me.core import Endpoint

adapter = TypeAdapter(OrderResponse)

class Get(Endpoint):
  async def get(self, id: str, *, validate: bool = True) -> OrderResponse:
    """Get order details by order identifier.
    
    - `id`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/trading-spot-rest#tag/trading/GET/v1/trading/order/{id})"""
    r = await self.authed_request('GET', f'/v1/trading/order/{id}')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

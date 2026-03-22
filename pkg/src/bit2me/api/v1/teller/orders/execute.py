from typing_extensions import TypedDict
from bit2me.core import AuthEndpoint

class TellerOrderExecuteRequest(TypedDict):
  orderId: str

class Execute(AuthEndpoint):
  async def execute(
    self,
    teller_order_execute_request: TellerOrderExecuteRequest,
    *,
    validate: bool = True
  ):
    """Execute a card order previously created with `POST /v1/teller/order/proforma`.
    
    - `teller_order_execute_request`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/funding/POST/v1/teller/order)"""
    r = await self.authed_request(
      'POST', '/v1/teller/order',
      json=teller_order_execute_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return r.json()

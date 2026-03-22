from typing_extensions import TypedDict
from bit2me.core import Endpoint

class TellerOrderCancelRequest(TypedDict):
  orderId: str
  description: str

class Cancel(Endpoint):
  async def cancel(
    self,
    teller_order_cancel_request: TellerOrderCancelRequest,
    *,
    validate: bool = True
  ):
    """Changes an order status from "waiting-user" to "cancelled" after the user accepting the transaction
    
    - `teller_order_cancel_request`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/funding/POST/v1/teller/order/cancel)"""
    r = await self.authed_request(
      'POST', '/v1/teller/order/cancel',
      json=teller_order_cancel_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return r.json()

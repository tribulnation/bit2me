from typing_extensions import NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class TellerOrderStatusResponse(TypedDict):
  status: NotRequired[str]
  """The status of the order (accepted or pending)"""

adapter = TypeAdapter(TellerOrderStatusResponse)

class GetStatus(Endpoint):
  async def get_status(self, *, id: str, validate: bool = True) -> TellerOrderStatusResponse:
    """Gets order status. If no order is found, "pending" status is returned as default value.
    
    - `id`: The order ID or the wallet proforma ID
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/funding/GET/v1/teller/order/status)"""
    params: dict = {
      'id': id,
    }
    r = await self.authed_request('GET', '/v1/teller/order/status', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

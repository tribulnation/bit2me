from typing_extensions import TypedDict
from bit2me.types import BooleanResultResponse
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class Entry(TypedDict):
  pocketId: str
  orderId: str

adapter = TypeAdapter(BooleanResultResponse)

class Claim(AuthEndpoint):
  async def claim(
    self,
    list_entry: list[Entry],
    *,
    validate: bool = True
  ) -> BooleanResultResponse:
    """Claim user pay orders
    
    - `list_entry`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/transfers/POST/v1/social-pay/order/claim)"""
    r = await self.authed_request(
      'POST', '/v1/social-pay/order/claim',
      json=list_entry
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

from typing_extensions import TypedDict
from bit2me.types import LoanAction
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class IncreaseGuaranteeRequest(TypedDict):
  guaranteeAmount: str

adapter = TypeAdapter(LoanAction)

class IncreaseGuarantee(AuthEndpoint):
  async def increase_guarantee(
    self,
    order_id: str,
    increase_guarantee_request: IncreaseGuaranteeRequest,
    *,
    validate: bool = True
  ) -> LoanAction:
    """Increase a loan order guarantee
    
    - `order_id`
    - `increase_guarantee_request`: data
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/loan/POST/v1/loan/orders/{orderId}/guarantee/increase)"""
    r = await self.authed_request(
      'POST', f'/v1/loan/orders/{order_id}/guarantee/increase',
      json=increase_guarantee_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

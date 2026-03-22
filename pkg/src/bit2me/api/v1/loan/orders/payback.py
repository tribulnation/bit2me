from typing_extensions import TypedDict
from bit2me.types import LoanAction
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class PaybackGuaranteeRequest(TypedDict):
  paybackAmount: str

adapter = TypeAdapter(LoanAction)

class Payback(Endpoint):
  async def payback(
    self,
    order_id: str,
    payback_guarantee_request: PaybackGuaranteeRequest,
    *,
    validate: bool = True
  ) -> LoanAction:
    """Process a payment to refund a specified amount of an loan. This action will complete the loan if the outstanding amount is fully paid.
    
    - `order_id`
    - `payback_guarantee_request`: data
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/loan/POST/v1/loan/orders/{orderId}/payback)"""
    r = await self.authed_request(
      'POST', f'/v1/loan/orders/{order_id}/payback',
      json=payback_guarantee_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

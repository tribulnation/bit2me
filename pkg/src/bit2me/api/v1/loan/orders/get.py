from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class LoanOrderResponse(TypedDict):
  orderId: NotRequired[str]
  createdAt: NotRequired[datetime]
  updatedAt: NotRequired[datetime]
  userId: NotRequired[str]
  requestedByUserId: NotRequired[str]
  guaranteeCurrency: NotRequired[str]
  guaranteeOriginalAmount: NotRequired[str]
  guaranteeAmount: NotRequired[str]
  loanCurrency: NotRequired[str]
  loanOriginalAmount: NotRequired[str]
  loanAmount: NotRequired[str]
  paybackAmount: NotRequired[str]
  ltv: NotRequired[str]
  apr: NotRequired[str]
  status: NotRequired[str]
  startedAt: NotRequired[datetime]
  finishedAt: NotRequired[datetime]
  expiresAt: NotRequired[datetime]
  paybackPrincipalAmount: NotRequired[str]
  paybackInterestAmount: NotRequired[str]
  interestAmount: NotRequired[str]
  loanAmountConverted: NotRequired[str]
  paybackAmountConverted: NotRequired[str]
  guaranteeAmountConverted: NotRequired[str]
  remainingAmount: NotRequired[str]
  remainingAmountConverted: NotRequired[str]
  remainingPrincipalAmount: NotRequired[str]
  remainingInterestAmount: NotRequired[str]
  liquidationPriceReference: NotRequired[str]
  discount: NotRequired[str]
  isUserApprovalRequired: NotRequired[bool]

adapter = TypeAdapter(LoanOrderResponse)

class Get(Endpoint):
  async def get(self, order_id: str, *, validate: bool = True) -> LoanOrderResponse:
    """Get a user loan order
    
    - `order_id`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/loan/GET/v1/loan/orders/{orderId})"""
    r = await self.authed_request('GET', f'/v1/loan/orders/{order_id}')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

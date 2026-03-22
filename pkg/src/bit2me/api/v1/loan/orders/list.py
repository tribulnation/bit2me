from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class DataItem(TypedDict):
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

class ListLoanOrdersResponse(TypedDict):
  total: NotRequired[int]
  data: NotRequired[list[DataItem]]

adapter = TypeAdapter(ListLoanOrdersResponse)

class List(AuthEndpoint):
  async def list(
    self,
    *,
    limit: float | None = None,
    offset: float | None = None,
    validate: bool = True
  ) -> ListLoanOrdersResponse:
    """Get user loan orders
    
    - `limit`
    - `offset`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/loan/GET/v1/loan/orders)"""
    params = {}
    if limit is not None:
      params['limit'] = limit
    if offset is not None:
      params['offset'] = offset
    r = await self.authed_request('GET', '/v1/loan/orders', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

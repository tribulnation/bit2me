from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class FeeAmountLiquidated(TypedDict):
  value: NotRequired[str]
  currency: NotRequired[str]
  converted: NotRequired[str]
  convertedCurrency: NotRequired[str]

class GuaranteeAmount(TypedDict):
  value: NotRequired[str]
  currency: NotRequired[str]
  converted: NotRequired[str]
  convertedCurrency: NotRequired[str]

class GuaranteeAmountLiquidated(TypedDict):
  value: NotRequired[str]
  currency: NotRequired[str]
  converted: NotRequired[str]
  convertedCurrency: NotRequired[str]

class LoanAmount(TypedDict):
  value: NotRequired[str]
  currency: NotRequired[str]
  converted: NotRequired[str]
  convertedCurrency: NotRequired[str]

class PaybackAmount(TypedDict):
  value: NotRequired[str]
  currency: NotRequired[str]
  converted: NotRequired[str]
  convertedCurrency: NotRequired[str]

class Payload(TypedDict):
  ltv: NotRequired[str]
  previousLtv: NotRequired[str]
  liquidationLtv: NotRequired[str]
  guaranteeAmount: NotRequired[GuaranteeAmount]
  isCompleted: NotRequired[bool]
  loanAmount: NotRequired[LoanAmount]
  paybackAmount: NotRequired[PaybackAmount]
  guaranteeAmountLiquidated: NotRequired[GuaranteeAmountLiquidated]
  feeAmountLiquidated: NotRequired[FeeAmountLiquidated]
  isPromotional: NotRequired[bool]

class DataItem(TypedDict):
  movementId: NotRequired[str]
  orderId: NotRequired[str]
  userId: NotRequired[str]
  type: NotRequired[str]
  createdAt: NotRequired[datetime]
  updatedAt: NotRequired[datetime]
  payload: NotRequired[Payload]

class ListLoanMovementsResponse(TypedDict):
  total: NotRequired[int]
  data: NotRequired[list[DataItem]]

adapter = TypeAdapter(ListLoanMovementsResponse)

class Movements(Endpoint):
  async def __call__(
    self,
    *,
    order_id: str | None = None,
    limit: float | None = None,
    offset: float | None = None,
    validate: bool = True
  ) -> ListLoanMovementsResponse:
    """Get loan user movements
    
    - `order_id`
    - `limit`
    - `offset`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/loan/GET/v1/loan/movements)"""
    params = {}
    if order_id is not None:
      params['orderId'] = order_id
    if limit is not None:
      params['limit'] = limit
    if offset is not None:
      params['offset'] = offset
    r = await self.authed_request('GET', '/v1/loan/movements', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

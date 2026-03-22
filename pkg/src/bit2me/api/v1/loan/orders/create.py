from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class CreateLoanRequest(TypedDict):
  guaranteeCurrency: str
  guaranteeAmount: str
  loanCurrency: str
  loanAmount: str

class CreateLoanResponse(TypedDict):
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

adapter = TypeAdapter(CreateLoanResponse)

class Create(Endpoint):
  async def create(
    self,
    create_loan_request: CreateLoanRequest,
    *,
    validate: bool = True
  ) -> CreateLoanResponse:
    """Create new loan
    
    - `create_loan_request`: data
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/loan/POST/v1/loan/orders)"""
    r = await self.authed_request(
      'POST', '/v1/loan/orders',
      json=create_loan_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

from typing_extensions import NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class LoanLtvResponse(TypedDict):
  guaranteeCurrency: NotRequired[str]
  guaranteeAmount: NotRequired[str]
  guaranteeAmountConverted: NotRequired[str]
  loanCurrency: NotRequired[str]
  loanAmount: NotRequired[str]
  loanAmountConverted: NotRequired[str]
  apr: NotRequired[str]
  ltv: NotRequired[str]
  userCurrency: NotRequired[str]

adapter = TypeAdapter(LoanLtvResponse)

class Ltv(Endpoint):
  async def __call__(
    self,
    *,
    guarantee_currency: str,
    guarantee_amount: str | None = None,
    loan_currency: str,
    loan_amount: str | None = None,
    user_currency: str,
    validate: bool = True
  ) -> LoanLtvResponse:
    """Get the calculated LTV (Loan To Value). You should provide one of (and only) loanAmount or guaranteeAmount
    
    - `guarantee_currency`
    - `guarantee_amount`
    - `loan_currency`
    - `loan_amount`
    - `user_currency`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/loan/GET/v1/loan/ltv)"""
    params: dict = {
      'guaranteeCurrency': guarantee_currency,
      'loanCurrency': loan_currency,
      'userCurrency': user_currency,
    }
    if guarantee_amount is not None:
      params['guaranteeAmount'] = guarantee_amount
    if loan_amount is not None:
      params['loanAmount'] = loan_amount
    r = await self.authed_request('GET', '/v1/loan/ltv', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class GuaranteeCurrenciesItem(TypedDict):
  currencyConfigurationGuaranteeId: NotRequired[str]
  currency: NotRequired[str]
  enabled: NotRequired[bool]
  liquidationLtv: NotRequired[str]
  initialLtv: NotRequired[str]
  createdAt: NotRequired[datetime]
  updatedAt: NotRequired[datetime]

class LoanCurrenciesItem(TypedDict):
  currencyConfigurationLoanId: NotRequired[str]
  currency: NotRequired[str]
  enabled: NotRequired[bool]
  liquidity: NotRequired[str]
  liquidityStatus: NotRequired[str]
  apr: NotRequired[str]
  minimumAmount: NotRequired[str]
  maximumAmount: NotRequired[str]
  createdAt: NotRequired[datetime]
  updatedAt: NotRequired[datetime]

class LoanCurrencyConfigResponse(TypedDict):
  loanCurrencies: NotRequired[list[LoanCurrenciesItem]]
  guaranteeCurrencies: NotRequired[list[GuaranteeCurrenciesItem]]

adapter = TypeAdapter(LoanCurrencyConfigResponse)

class Currencies(AuthEndpoint):
  async def currencies(self, *, validate: bool = True) -> LoanCurrencyConfigResponse:
    """Get the configuration of loan currencies. This includes which currencies are available for loans and which can be used as guarantee
    
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/loan/GET/v2/loan/currency/configuration)"""
    r = await self.authed_request('GET', '/v2/loan/currency/configuration')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

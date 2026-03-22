from typing_extensions import TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class EarnUserSummaryResponse(TypedDict):
  currency: str
  totalBalance: float
  totalRewards: float

adapter = TypeAdapter(EarnUserSummaryResponse)

class Summary(Endpoint):
  async def __call__(
    self,
    *,
    user_currency: str | None = None,
    validate: bool = True
  ) -> EarnUserSummaryResponse:
    """Retrieves user summary
    
    - `user_currency`: Currency to show balance
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/earn/GET/v1/earn/summary)"""
    params = {}
    if user_currency is not None:
      params['userCurrency'] = user_currency
    r = await self.authed_request('GET', '/v1/earn/summary', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

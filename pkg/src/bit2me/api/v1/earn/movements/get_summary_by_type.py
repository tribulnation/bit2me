from typing_extensions import Literal, NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class Converted(TypedDict):
  amount: NotRequired[str]
  currency: NotRequired[str]

class TotalConverted(TypedDict):
  amount: float
  currency: str

class Entry(TypedDict):
  type: str
  currency: str
  total: str
  totalConverted: NotRequired[TotalConverted]
  converted: NotRequired[Converted]

adapter = TypeAdapter(list[Entry])

class GetSummaryByType(AuthEndpoint):
  async def get_summary_by_type(
    self,
    type: Literal['deposit', 'reward', 'withdrawal'],
    *,
    user_currency: str | None = None,
    rate_moment: Literal['creation', 'current'],
    order: Literal['desc', 'asc'],
    validate: bool = True
  ) -> list[Entry]:
    """Retrieves summary of movements per operation (deposit, reward, withdrawal)
    
    - `type`: Operation type
    - `user_currency`: Currency to show balance
    - `rate_moment`: Rate moment
    - `order`: Sorting direction
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/earn/GET/v1/earn/movements/{type}/summary)"""
    params: dict = {
      'rateMoment': rate_moment,
      'order': order,
    }
    if user_currency is not None:
      params['userCurrency'] = user_currency
    r = await self.authed_request(
      'GET', f'/v1/earn/movements/{type}/summary',
      params=params
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

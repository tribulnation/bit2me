from typing_extensions import Literal
from bit2me.types import EarnWalletResponse
from pydantic import TypeAdapter
from bit2me.core import Endpoint

adapter = TypeAdapter(EarnWalletResponse)

class Wallets(Endpoint):
  async def wallets(
    self,
    *,
    user_currency: str | None = None,
    sort_by: Literal['currency', 'balance'] | None = None,
    sort_direction: Literal['ascending', 'descending'] | None = None,
    offset: int | None = None,
    limit: int | None = None,
    validate: bool = True
  ) -> EarnWalletResponse:
    """Get a list of earn wallets
    
    - `user_currency`: Currency to show convertedBalance
    - `sort_by`: Sorting field
    - `sort_direction`: Sorting direction
    - `offset`
    - `limit`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/earn/GET/v2/earn/wallets)"""
    params = {}
    if user_currency is not None:
      params['userCurrency'] = user_currency
    if sort_by is not None:
      params['sortBy'] = sort_by
    if sort_direction is not None:
      params['sortDirection'] = sort_direction
    if offset is not None:
      params['offset'] = offset
    if limit is not None:
      params['limit'] = limit
    r = await self.authed_request('GET', '/v2/earn/wallets', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

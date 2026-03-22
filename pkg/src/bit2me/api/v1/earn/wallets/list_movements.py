from datetime import datetime
from typing_extensions import Any, Literal, NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class Amount(TypedDict):
  value: NotRequired[str]
  currency: NotRequired[str]

class DataItem(TypedDict):
  movementId: NotRequired[str]
  userId: NotRequired[str]
  type: NotRequired[Literal['deposit', 'withdrawal', 'reward']]
  status: NotRequired[str]
  createdAt: NotRequired[datetime]
  updatedAt: NotRequired[datetime]
  walletId: NotRequired[str]
  lockId: NotRequired[str | None]
  amount: NotRequired[Amount]
  withholdingAmount: NotRequired[dict[str, Any]]
  netAmount: NotRequired[dict[str, Any]]
  rate: NotRequired[dict[str, Any]]
  convertedAmount: NotRequired[dict[str, Any]]
  source: NotRequired[dict[str, Any] | None]
  issuer: NotRequired[dict[str, Any]]

class ListEarnWalletMovementsResponse(TypedDict):
  total: int
  """Total movements matching the query"""
  data: list[DataItem]
  """Earn movements returned"""

adapter = TypeAdapter(ListEarnWalletMovementsResponse)

class ListMovements(AuthEndpoint):
  async def list_movements(
    self,
    wallet_id: str,
    *,
    user_currency: str | None = None,
    offset: int | None = None,
    limit: int | None = None,
    sort_by: Literal['createdAt'] | None = None,
    sort_direction: Literal['ascending', 'descending'] | None = None,
    validate: bool = True
  ) -> ListEarnWalletMovementsResponse:
    """Retrieve the wallet movement list.
    
    Movements can be paginated with `offset` and `limit`. For example, to fetch the third page with 20 records per page:
    
    ```text
    /v1/earn/wallets/{walletId}/movements?offset=40&limit=20
    ```
    
    - `wallet_id`: Wallet identifier
    - `user_currency`: Currency to show convertedAmount
    - `offset`: Specify the number of entries to be skipped (0 by default)
    - `limit`: Specify the maximum number of entries to be returned (20 by default)
    - `sort_by`: Sorting field
    - `sort_direction`: Sorting direction
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/earn/GET/v1/earn/wallets/{walletId}/movements)"""
    params = {}
    if user_currency is not None:
      params['userCurrency'] = user_currency
    if offset is not None:
      params['offset'] = offset
    if limit is not None:
      params['limit'] = limit
    if sort_by is not None:
      params['sortBy'] = sort_by
    if sort_direction is not None:
      params['sortDirection'] = sort_direction
    r = await self.authed_request(
      'GET', f'/v1/earn/wallets/{wallet_id}/movements',
      params=params
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

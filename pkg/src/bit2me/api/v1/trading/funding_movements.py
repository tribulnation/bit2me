from datetime import datetime
from typing_extensions import Any, Literal, NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class Entry(TypedDict):
  id: NotRequired[str]
  movementType: NotRequired[Literal['deposit', 'withdrawal']]
  amount: NotRequired[float]
  createdAt: NotRequired[datetime]
  walletId: NotRequired[str]
  currency: NotRequired[str]
  status: NotRequired[Literal['pending', 'completed', 'canceled']]
  serviceOrderName: NotRequired[Literal['wallet', 'admin', 'working-capital']]

adapter = TypeAdapter(list[Entry])

class FundingMovements(Endpoint):
  async def __call__(
    self,
    *,
    wallet_id: Any | None = None,
    currency: Any | None = None,
    from_: Any | None = None,
    to: Any | None = None,
    service_order_name: Any | None = None,
    movement_type: Any | None = None,
    limit: Any | None = None,
    validate: bool = True
  ) -> list[Entry]:
    """Get funding movements
    
    - `wallet_id`: Wallet id
    - `currency`: Currency
    - `from_`: The initial date with time
    - `to`: The end date with time
    - `service_order_name`: Service order name (issuer)
    - `movement_type`: Movement type
    - `limit`: The maximum number of movements returned
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/trading-spot-rest#tag/funding/GET/v1/trading/movement)"""
    params = {}
    if wallet_id is not None:
      params['walletId'] = wallet_id
    if currency is not None:
      params['currency'] = currency
    if from_ is not None:
      params['from'] = from_
    if to is not None:
      params['to'] = to
    if service_order_name is not None:
      params['serviceOrderName'] = service_order_name
    if movement_type is not None:
      params['movementType'] = movement_type
    if limit is not None:
      params['limit'] = limit
    r = await self.authed_request('GET', '/v1/trading/movement', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

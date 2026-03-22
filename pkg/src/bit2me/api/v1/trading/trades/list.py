from datetime import datetime
from typing_extensions import Any, NotRequired, TypedDict
from bit2me.types import (
  OffsetParam,
  OrderSide,
  OrderType,
  SortDirectionParam,
  TradeResponse
)
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class ListTradingTradesResponse(TypedDict):
  count: NotRequired[float]
  data: NotRequired[list[TradeResponse]]

adapter = TypeAdapter(ListTradingTradesResponse)

class List(AuthEndpoint):
  async def list(
    self,
    *,
    ids: Any | None = None,
    symbol: str | None = None,
    side: OrderSide | None = None,
    order_type: OrderType | None = None,
    limit: float | None = None,
    offset: OffsetParam | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    sort: str | None = None,
    direction: SortDirectionParam | None = None,
    validate: bool = True
  ) -> ListTradingTradesResponse:
    """Get all user trades paged with a maximum page size of 50.
    The result can be filtered by dates and side optionally.
    
    - `ids`: Comma separated trade identifiers
    - `symbol`
    - `side`
    - `order_type`
    - `limit`: The maximum number of trades to fetch
    - `offset`
    - `start_time`
    - `end_time`
    - `sort`: The field to sort
    - `direction`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/trading-spot-rest#tag/trading/GET/v1/trading/trade)"""
    params = {}
    if ids is not None:
      params['ids'] = ids
    if symbol is not None:
      params['symbol'] = symbol
    if side is not None:
      params['side'] = side
    if order_type is not None:
      params['orderType'] = order_type
    if limit is not None:
      params['limit'] = limit
    if offset is not None:
      params['offset'] = offset
    if start_time is not None:
      params['startTime'] = start_time
    if end_time is not None:
      params['endTime'] = end_time
    if sort is not None:
      params['sort'] = sort
    if direction is not None:
      params['direction'] = direction
    r = await self.authed_request('GET', '/v1/trading/trade', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

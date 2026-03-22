from datetime import datetime
from typing_extensions import Any
from bit2me.types import (
  OffsetParam,
  OrderResponse,
  OrderSide,
  OrderStatus,
  OrderType,
  SortDirectionParam
)
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

adapter = TypeAdapter(list[OrderResponse])

class List(AuthEndpoint):
  async def list(
    self,
    *,
    ids: Any | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    side: OrderSide | None = None,
    symbol: str | None = None,
    order_type: OrderType | None = None,
    status: OrderStatus | None = None,
    status_ne: str | None = None,
    status_in: str | None = None,
    status_ni: str | None = None,
    limit: float | None = None,
    offset: OffsetParam | None = None,
    sort: str | None = None,
    direction: SortDirectionParam | None = None,
    client_order_id: Any | None = None,
    validate: bool = True
  ) -> list[OrderResponse]:
    """Get all user orders paged with a maximum page size of 100. The result can be filtered by dates, list of statuses,
    side and market symbol optionally.
    
    - `ids`: Comma separated order identifiers
    - `start_time`
    - `end_time`
    - `side`
    - `symbol`
    - `order_type`
    - `status`
    - `status_ne`: Comma separated NOT EQUAL order statuses
    - `status_in`: Comma separated IN order statuses
    - `status_ni`: Comma separated NOT IN order statuses
    - `limit`: The maximum number of orders retrieved
    - `offset`
    - `sort`: Field name to sort
    - `direction`
    - `client_order_id`: Comma separated client order identifiers
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/trading-spot-rest#tag/trading/GET/v1/trading/order)"""
    params = {}
    if ids is not None:
      params['ids'] = ids
    if start_time is not None:
      params['startTime'] = start_time
    if end_time is not None:
      params['endTime'] = end_time
    if side is not None:
      params['side'] = side
    if symbol is not None:
      params['symbol'] = symbol
    if order_type is not None:
      params['orderType'] = order_type
    if status is not None:
      params['status'] = status
    if status_ne is not None:
      params['status_ne'] = status_ne
    if status_in is not None:
      params['status_in'] = status_in
    if status_ni is not None:
      params['status_ni'] = status_ni
    if limit is not None:
      params['limit'] = limit
    if offset is not None:
      params['offset'] = offset
    if sort is not None:
      params['sort'] = sort
    if direction is not None:
      params['direction'] = direction
    if client_order_id is not None:
      params['clientOrderId'] = client_order_id
    r = await self.authed_request('GET', '/v1/trading/order', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

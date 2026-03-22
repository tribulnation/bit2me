from bit2me.types import OrderSide
from pydantic import TypeAdapter
from bit2me.core import Endpoint

adapter = TypeAdapter(list[list[OrderSide | float]])

class GetLast(Endpoint):
  async def get_last(
    self,
    *,
    symbol: str,
    limit: float | None = None,
    validate: bool = True
  ) -> list[list[OrderSide | float]]:
    """Get a list of last trades. Returns the last 50 trades by default.
    
    - `symbol`
    - `limit`: The number of trades to retrieve
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/trading-spot-rest#tag/marketdata/GET/v1/trading/trade/last)"""
    params: dict = {
      'symbol': symbol,
    }
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', '/v1/trading/trade/last', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

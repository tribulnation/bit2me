from typing_extensions import NotRequired, TypedDict
from bit2me.types import MillisTimestamp
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class TradingOrderBookResponse(TypedDict):
  asks: NotRequired[list[list[float]]]
  """Entries containing sell orders with price and volume"""
  bids: NotRequired[list[list[float]]]
  """Entries containing buy orders with price and volume"""
  timestamp: NotRequired[MillisTimestamp]
  symbol: NotRequired[str]
  """Market symbol"""

adapter = TypeAdapter(TradingOrderBookResponse)

class OrderBook(Endpoint):
  async def order_book(
    self,
    *,
    symbol: str,
    validate: bool = True
  ) -> TradingOrderBookResponse:
    """Get the order book associated to the market symbol.
    
    - `symbol`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/trading-spot-rest#tag/marketdata/GET/v2/trading/order-book)"""
    params: dict = {
      'symbol': symbol,
    }
    r = await self.request('GET', '/v2/trading/order-book', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

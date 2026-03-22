from typing_extensions import NotRequired, TypedDict
from bit2me.types import MillisTimestamp
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class Entry(TypedDict):
  timestamp: NotRequired[MillisTimestamp]
  symbol: NotRequired[str]
  """Market symbol"""
  open: NotRequired[float]
  """Opening price (price 24 horus ago)"""
  bid: NotRequired[float]
  """Highest price a buyer will pay for order"""
  ask: NotRequired[float]
  """Lowest price a seller will take for order"""
  close: NotRequired[float]
  """Closing price (last trade price)"""
  high: NotRequired[float]
  """Highest price in the last 24 hours"""
  low: NotRequired[float]
  """Lowest price in the last 24 hours"""
  percentage: NotRequired[float]
  """Percentage of current price versus opening price"""
  baseVolume: NotRequired[float]
  """Volume traded in terms of the base currency"""
  quoteVolume: NotRequired[float]
  """Volume traded in terms of the quote currency"""

adapter = TypeAdapter(list[Entry])

class Tickers(Endpoint):
  async def tickers(self, *, symbol: str | None = None, validate: bool = True) -> list[Entry]:
    """Get ticker information (OHLCV, current best bid and ask, percentage versus price 24 hours ago) for all markets or by requested market symbol. The data refers to the last 24 hours from the date indicated by the timestamp.
    
    - `symbol`: Market symbol (optional, default all markets)
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/trading-spot-rest#tag/marketdata/GET/v2/trading/tickers)"""
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    r = await self.request('GET', '/v2/trading/tickers', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

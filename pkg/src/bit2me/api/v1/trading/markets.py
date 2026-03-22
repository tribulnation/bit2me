from datetime import datetime
from typing_extensions import Literal, NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class Entry(TypedDict):
  id: NotRequired[str]
  """Market identifier"""
  symbol: NotRequired[str]
  """Market symbol"""
  minAmount: NotRequired[float]
  """Minimum order amount (in terms of base currency)"""
  maxAmount: NotRequired[float]
  """Maximum order amount (in terms of base currency)"""
  minPrice: NotRequired[float]
  """Minimum order price (in terms of quote currency)"""
  maxPrice: NotRequired[float]
  """Maximum order price (in terms of quote currency)"""
  minOrderSize: NotRequired[float]
  """Minimum order size (in terms of base amount per quote price)"""
  pricePrecision: NotRequired[float]
  """Scaling decimals places for price"""
  tickSize: NotRequired[float]
  """Decimal number representing scaling decimals places for price"""
  amountPrecision: NotRequired[float]
  """Scaling decimals places for amount"""
  marketEnabled: NotRequired[Literal['enabled', 'enabled_at', 'frozen', 'disabled']]
  """The current status of the market. The market can be enabled, disabled, enabled at specified date in the `marketEnabledAt` field, or frozen, which does not allow orders to be added or deleted"""
  marketEnabledAt: NotRequired[datetime | None]
  """Date time in ISO 8601 string format"""
  initialPrice: NotRequired[float]
  """Initial market price. If the market is not yet enabled, the orders must take that reference price to be placed above or below"""

adapter = TypeAdapter(list[Entry])

class Markets(Endpoint):
  async def __call__(
    self,
    *,
    symbol: str | None = None,
    validate: bool = True
  ) -> list[Entry]:
    """Get a list of markets (quantity and price precisions, order minimums and maximums, status).
    
    - `symbol`: The market symbol to filter (optional, by default returns all markets)
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/trading-spot-rest#tag/marketdata/GET/v1/trading/market-config)"""
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    r = await self.request('GET', '/v1/trading/market-config', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

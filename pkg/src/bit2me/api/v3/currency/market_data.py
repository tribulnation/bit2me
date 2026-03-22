from typing_extensions import TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class CurrencyMarketDataV3response(TypedDict):
  marketCap: str
  totalVolume: str
  fullyDilutedMarketCap: str
  maxSupply: int
  totalSupply: int

adapter = TypeAdapter(CurrencyMarketDataV3response)

class MarketData(Endpoint):
  async def market_data(
    self,
    symbol: str,
    *,
    validate: bool = True
  ) -> CurrencyMarketDataV3response:
    """Returns the market data for given currency in USD
    
    - `symbol`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/market/GET/v3/currency/market-data/{symbol})"""
    r = await self.authed_request('GET', f'/v3/currency/market-data/{symbol}')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

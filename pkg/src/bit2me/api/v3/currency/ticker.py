from typing_extensions import NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class Point(TypedDict):
  time: int
  price: str
  interval: str
  marketCap: NotRequired[str]
  totalVolume: NotRequired[str]
  fullyDilutedMarketCap: NotRequired[str]
  maxSupply: NotRequired[str]
  totalSupply: NotRequired[str]

adapter = TypeAdapter(dict[str, dict[str, list[Point]]])

class Ticker(Endpoint):
  async def ticker(
    self,
    symbol: str,
    *,
    rate_currency: str | None = None,
    interval: list[str] | None = None,
    extended: bool | None = None,
    validate: bool = True
  ) -> dict[str, dict[str, list[Point]]]:
    """Return ticker data for the selected cryptocurrency.
    
    - `symbol`
    - `rate_currency`
    - `interval`
    - `extended`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/market/GET/v3/currency/ticker/{symbol})"""
    params = {}
    if rate_currency is not None:
      params['rateCurrency'] = rate_currency
    if interval is not None:
      params['interval'] = interval
    if extended is not None:
      params['extended'] = extended
    r = await self.authed_request(
      'GET', f'/v3/currency/ticker/{symbol}',
      params=params
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

from datetime import datetime
from typing_extensions import Literal, TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class CurrencyOhlcResponse(TypedDict):
  open: str
  high: str
  low: str
  close: str
  average: str

adapter = TypeAdapter(CurrencyOhlcResponse)

class Ohlca(AuthEndpoint):
  async def ohlca(
    self,
    symbol: str,
    *,
    time: datetime | None = None,
    timeframe: Literal['1H', '4H', '12H', '1D', '1W', '1M', '1Y'],
    validate: bool = True
  ) -> CurrencyOhlcResponse:
    """Returns OHLCA for the given symbol
    
    - `symbol`
    - `time`
    - `timeframe`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/market/GET/v1/currency/ohlca/{symbol})"""
    params: dict = {
      'timeframe': timeframe,
    }
    if time is not None:
      params['time'] = time
    r = await self.authed_request(
      'GET', f'/v1/currency/ohlca/{symbol}',
      params=params
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

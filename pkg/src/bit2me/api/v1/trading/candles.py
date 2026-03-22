from datetime import datetime
from typing_extensions import Literal
from bit2me.types import MillisTimestamp
from bit2me.core import Endpoint, timestamp as ts
from pydantic import TypeAdapter

adapter = TypeAdapter(list[list[float]])

class Candles(Endpoint):
  async def __call__(
    self,
    *,
    symbol: str,
    interval: Literal[1, 5, 15, 30, 60, 240, 1440],
    start_time: MillisTimestamp | datetime,
    end_time: MillisTimestamp | datetime,
    limit: float,
    validate: bool = True
  ) -> list[list[float]]:
    """Get OHLCV (open, highest, lowest, close, volume) information. The last entry in the OHLCV array is for the current.
    
    - `symbol`
    - `interval`
    - `start_time`
    - `end_time`
    - `limit`: The limit of `interval` entries (with an `interval` of 15 minutes and `limit` 4 the response is the last hour with 4 entries)
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/trading-spot-rest#tag/marketdata/GET/v1/trading/candle)"""
    params: dict = {
      'symbol': symbol,
      'interval': interval,
      'startTime': ts.dump(start_time),
      'endTime': ts.dump(end_time),
      'limit': limit,
    }
    r = await self.request('GET', '/v1/trading/candle', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

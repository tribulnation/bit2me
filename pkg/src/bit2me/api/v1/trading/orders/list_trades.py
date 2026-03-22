from bit2me.types import TradeResponse
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

adapter = TypeAdapter(list[TradeResponse])

class ListTrades(AuthEndpoint):
  async def list_trades(self, id: str, *, validate: bool = True) -> list[TradeResponse]:
    """Get all trades associated to the order.
    
    - `id`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/trading-spot-rest#tag/trading/GET/v1/trading/order/{id}/trades)"""
    r = await self.authed_request('GET', f'/v1/trading/order/{id}/trades')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

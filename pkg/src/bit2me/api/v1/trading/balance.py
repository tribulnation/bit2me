from typing_extensions import Any
from bit2me.types import WalletResponse
from pydantic import TypeAdapter
from bit2me.core import Endpoint

adapter = TypeAdapter(list[WalletResponse])

class Balance(Endpoint):
  async def __call__(
    self,
    *,
    symbols: Any | None = None,
    validate: bool = True
  ) -> list[WalletResponse]:
    """Retrieve balances of all wallets and blocked balances in active orders.
    
    - `symbols`: Comma separated symbols of the wallets that you want to retrieve
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/trading-spot-rest#tag/funding/GET/v1/trading/wallet/balance)"""
    params = {}
    if symbols is not None:
      params['symbols'] = symbols
    r = await self.authed_request(
      'GET', '/v1/trading/wallet/balance',
      params=params
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

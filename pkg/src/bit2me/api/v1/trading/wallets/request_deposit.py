from typing_extensions import TypedDict
from bit2me.types import WalletResponse
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class TradingWalletDepositRequest(TypedDict):
  fromPocketId: str
  """Bit2Me pocket identifier"""
  amount: str
  currency: str
  """Valid currency symbol"""

adapter = TypeAdapter(WalletResponse)

class RequestDeposit(Endpoint):
  async def request_deposit(
    self,
    trading_wallet_deposit_request: TradingWalletDepositRequest,
    *,
    validate: bool = True
  ) -> WalletResponse:
    """Request deposit funds into your Pro account from a Bit2Me Wallet.
    
    - `trading_wallet_deposit_request`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/trading-spot-rest#tag/funding/POST/v1/trading/wallet/deposit)"""
    r = await self.authed_request(
      'POST', '/v1/trading/wallet/deposit',
      json=trading_wallet_deposit_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

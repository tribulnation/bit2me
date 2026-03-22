from typing_extensions import NotRequired, TypedDict
from bit2me.types import WalletResponse
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class TradingWalletWithdrawalRequest(TypedDict):
  toPocketId: NotRequired[str]
  """Bit2Me pocket identifier"""
  amount: str
  currency: str
  """Valid currency symbol"""

adapter = TypeAdapter(WalletResponse)

class RequestWithdrawal(AuthEndpoint):
  async def request_withdrawal(
    self,
    trading_wallet_withdrawal_request: TradingWalletWithdrawalRequest,
    *,
    validate: bool = True
  ) -> WalletResponse:
    """Request a withdrawal from the Pro account to the Bit2Me wallet.
    
    - `trading_wallet_withdrawal_request`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/trading-spot-rest#tag/funding/POST/v1/trading/wallet/withdraw)"""
    r = await self.authed_request(
      'POST', '/v1/trading/wallet/withdraw',
      json=trading_wallet_withdrawal_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

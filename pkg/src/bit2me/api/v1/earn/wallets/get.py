from bit2me.types import EarnWalletRecord
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

adapter = TypeAdapter(EarnWalletRecord)

class Get(AuthEndpoint):
  async def get(
    self,
    wallet_id: str,
    *,
    user_currency: str | None = None,
    validate: bool = True
  ) -> EarnWalletRecord:
    """Retrieves full information of selected wallet
    
    - `wallet_id`: Wallet identifier
    - `user_currency`: Currency to show convertedBalance
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/earn/GET/v1/earn/wallets/{walletId})"""
    params = {}
    if user_currency is not None:
      params['userCurrency'] = user_currency
    r = await self.authed_request(
      'GET', f'/v1/earn/wallets/{wallet_id}',
      params=params
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

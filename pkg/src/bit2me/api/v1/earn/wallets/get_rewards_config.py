from bit2me.types import EarnRewardsConfigResponse
from pydantic import TypeAdapter
from bit2me.core import Endpoint

adapter = TypeAdapter(EarnRewardsConfigResponse)

class GetRewardsConfig(Endpoint):
  async def get_rewards_config(
    self,
    wallet_id: str,
    *,
    validate: bool = True
  ) -> EarnRewardsConfigResponse:
    """Retrieves rewards configuration for selected wallet
    
    - `wallet_id`: Wallet identifier
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/earn/GET/v1/earn/wallets/{walletId}/rewards/config)"""
    r = await self.authed_request(
      'GET', f'/v1/earn/wallets/{wallet_id}/rewards/config'
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

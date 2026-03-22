from typing_extensions import TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class UpdateEarnWalletRewardCurrencyRequest(TypedDict):
  rewardCurrency: str
  """Currency to obtain the reward"""

class UpdateEarnWalletRewardCurrencyResponse(TypedDict):
  result: bool

adapter = TypeAdapter(UpdateEarnWalletRewardCurrencyResponse)

class UpdateRewardsConfig(Endpoint):
  async def update_rewards_config(
    self,
    wallet_id: str,
    update_earn_wallet_reward_currency_request: UpdateEarnWalletRewardCurrencyRequest,
    *,
    validate: bool = True
  ) -> UpdateEarnWalletRewardCurrencyResponse:
    """Update wallet reward configuration for selected wallet
    
    - `wallet_id`: Wallet identifier
    - `update_earn_wallet_reward_currency_request`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/earn/PATCH/v1/earn/wallets/{walletId}/rewards/config)"""
    r = await self.authed_request(
      'PATCH', f'/v1/earn/wallets/{wallet_id}/rewards/config',
      json=update_earn_wallet_reward_currency_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

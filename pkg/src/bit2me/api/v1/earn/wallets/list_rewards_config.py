from datetime import datetime
from typing_extensions import TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class Entry(TypedDict):
  walletId: str
  userId: str
  currency: str
  lockPeriodId: str | None
  rewardCurrency: str
  createdAt: datetime
  updatedAt: datetime

adapter = TypeAdapter(list[Entry])

class ListRewardsConfig(AuthEndpoint):
  async def list_rewards_config(self, *, validate: bool = True) -> list[Entry]:
    """Retrieves rewards configuration for user wallets
    
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/earn/GET/v1/earn/wallets/rewards/config)"""
    r = await self.authed_request('GET', '/v1/earn/wallets/rewards/config')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

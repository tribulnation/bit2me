from bit2me.core import AuthEndpoint

class GetRewardsSummary(AuthEndpoint):
  async def get_rewards_summary(
    self,
    wallet_id: str,
    *,
    user_currency: str | None = None,
    validate: bool = True
  ):
    """Retrieves full list of rewards summary for selected wallet
    
    - `wallet_id`: Wallet identifier
    - `user_currency`: Currency to show balance
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/earn/GET/v1/earn/wallets/{walletId}/rewards/summary)"""
    params = {}
    if user_currency is not None:
      params['userCurrency'] = user_currency
    r = await self.authed_request(
      'GET', f'/v1/earn/wallets/{wallet_id}/rewards/summary',
      params=params
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return r.json()

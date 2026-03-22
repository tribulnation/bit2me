from typing_extensions import Literal, NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class RewardAllowedItem(TypedDict):
  currency: NotRequired[str]
  """Currency where can receive rewards"""
  extraYield: NotRequired[float]
  """Extra Yield by currency applied in the reward"""
  type: NotRequired[Literal['daily', 'weekly', 'monthly']]
  """Reward type"""

class Entry(TypedDict):
  currency: NotRequired[str]
  """Currency symbol, it should be an allowed currency"""
  disabled: NotRequired[bool]
  """Currency status on earn"""
  isNew: NotRequired[bool]
  """Currency added on earn in the last 7 days"""
  currenciesRewardAllowed: NotRequired[list[RewardAllowedItem]]
  """Currency rewards allowed with their info"""
  levelExtraYieldType: NotRequired[Literal['space-pool', 'provided']]

adapter = TypeAdapter(list[Entry])

class Assets(Endpoint):
  async def assets(
    self,
    *,
    type: Literal['partner', 'farming-pool'] | None = None,
    validate: bool = True
  ) -> list[Entry]:
    """Retrieves full list of supported assets in earn service
    
    - `type`: Asset type
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/earn/GET/v2/earn/assets)"""
    params = {}
    if type is not None:
      params['type'] = type
    r = await self.request('GET', '/v2/earn/assets', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

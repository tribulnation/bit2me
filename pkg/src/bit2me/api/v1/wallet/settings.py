from typing_extensions import Any, NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class Entry(TypedDict):
  symbol: str
  """Valid currency symbol"""
  actions: list[str]
  limit: NotRequired[dict[str, Any]]

adapter = TypeAdapter(list[Entry])

class Settings(Endpoint):
  async def __call__(self, *, validate: bool = True) -> list[Entry]:
    """Get asset settings
    
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/wallet/GET/v1/wallet/settings/assets)"""
    r = await self.request('GET', '/v1/wallet/settings/assets')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

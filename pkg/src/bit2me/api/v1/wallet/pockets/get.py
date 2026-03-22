from datetime import datetime
from typing_extensions import TypedDict
from bit2me.types import PocketColor
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class Entry(TypedDict):
  id: str
  name: str
  color: PocketColor
  currency: str
  """Valid currency symbol"""
  balance: str
  blockedBalance: str
  createdAt: datetime
  """When the pocket was created (ISO 8601)"""

adapter = TypeAdapter(list[Entry])

class Get(Endpoint):
  async def get(self, *, id: str | None = None, validate: bool = True) -> list[Entry]:
    """Get the data of a specific pocket or the data of all pockets of the user (if the *id* param is not set)
    
    - `id`: With this parameter you can specify the pocket you want to get the data from.
    If this parameter is not set, all pockets of the user are returned
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/wallet/GET/v1/wallet/pocket)"""
    params = {}
    if id is not None:
      params['id'] = id
    r = await self.authed_request('GET', '/v1/wallet/pocket', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

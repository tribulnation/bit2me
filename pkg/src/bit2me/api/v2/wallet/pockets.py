from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class Entry(TypedDict):
  id: NotRequired[str]
  createdAt: NotRequired[datetime]
  """When the address was created (ISO 8601)"""
  address: NotRequired[str]
  network: NotRequired[str]
  """The destination address network"""
  tag: NotRequired[str | None]

adapter = TypeAdapter(list[Entry])

class Pockets(AuthEndpoint):
  async def pockets(
    self,
    pocket_id: str,
    network: str,
    *,
    validate: bool = True
  ) -> list[Entry]:
    """Find all address by pocket ID and Network or create one new
    
    - `pocket_id`
    - `network`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/wallet/GET/v2/wallet/pocket/{pocketId}/{network}/address)"""
    r = await self.authed_request(
      'GET', f'/v2/wallet/pocket/{pocket_id}/{network}/address'
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

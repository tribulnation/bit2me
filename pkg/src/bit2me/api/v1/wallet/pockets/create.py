from typing_extensions import TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class CreatePocketRequest(TypedDict):
  currency: str
  """Valid currency symbol"""
  name: str

class CreatePocketResponse(TypedDict):
  id: str

adapter = TypeAdapter(CreatePocketResponse)

class Create(Endpoint):
  async def create(
    self,
    create_pocket_request: CreatePocketRequest,
    *,
    validate: bool = True
  ) -> CreatePocketResponse:
    """Create a new pocket
    
    - `create_pocket_request`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/wallet/POST/v1/wallet/pocket)"""
    r = await self.authed_request(
      'POST', '/v1/wallet/pocket',
      json=create_pocket_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

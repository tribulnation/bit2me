from typing_extensions import NotRequired, TypedDict
from bit2me.types import BooleanResultResponse, PocketColor
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class UpdateWalletPocketRequest(TypedDict):
  id: str
  name: NotRequired[str]
  color: NotRequired[PocketColor]

adapter = TypeAdapter(BooleanResultResponse)

class Update(Endpoint):
  async def update(
    self,
    update_wallet_pocket_request: UpdateWalletPocketRequest,
    *,
    validate: bool = True
  ) -> BooleanResultResponse:
    """Update pocket data
    
    - `update_wallet_pocket_request`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/wallet/PUT/v1/wallet/pocket)"""
    r = await self.authed_request(
      'put', '/v1/wallet/pocket',
      json=update_wallet_pocket_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

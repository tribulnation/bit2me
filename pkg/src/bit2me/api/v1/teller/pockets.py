from typing_extensions import Any, TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class Pocket(TypedDict):
  userId: str
  pocketId: str
  reference: str

class TellerPocketReferenceResponse(TypedDict):
  pocket: Pocket
  bankAccounts: dict[str, Any]

adapter = TypeAdapter(TellerPocketReferenceResponse)

class Pockets(AuthEndpoint):
  async def __call__(
    self,
    *,
    pocket_id: str,
    validate: bool = True
  ) -> TellerPocketReferenceResponse:
    """Returns a reference for the specified pocket. Reference is generated if it doesn't exist.
    
    - `pocket_id`: Id of the pocket to retrieve the reference from
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/funding/GET/v1/teller/pocket/reference)"""
    params: dict = {
      'pocketId': pocket_id,
    }
    r = await self.authed_request(
      'GET', '/v1/teller/pocket/reference',
      params=params
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

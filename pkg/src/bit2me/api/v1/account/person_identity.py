from datetime import datetime
from typing_extensions import Literal, TypedDict
from bit2me.types import BooleanResultResponse
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class UpdatePersonIdentityRequest(TypedDict):
  type: Literal['none', 'idcard', 'passport', 'drivinglicense', 'visa']
  number: str
  expiryDate: datetime
  countryCode: str

adapter = TypeAdapter(BooleanResultResponse)

class PersonIdentity(AuthEndpoint):
  async def __call__(
    self,
    update_person_identity_request: UpdatePersonIdentityRequest,
    *,
    validate: bool = True
  ) -> BooleanResultResponse:
    """Update user person identity
    
    - `update_person_identity_request`: The details to update user person identity
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/PUT/v1/account/users/person/identity)"""
    r = await self.authed_request(
      'put', '/v1/account/users/person/identity',
      json=update_person_identity_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

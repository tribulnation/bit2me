from typing_extensions import NotRequired, TypedDict
from bit2me.types import UserAddress
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class UserAddressBody(TypedDict):
  id: NotRequired[str]
  userId: NotRequired[str]
  alias: NotRequired[str]
  streetAddress: str
  city: str
  stateCode: str
  """Value obtained from 'fips' (Federal Information Processing Standard  (https://en.wikipedia.org/wiki/Federal_Information_Processing_Standards)) field in /v1/misc/country/{countryISOCode}/region response.

  Additional information of this endpoint is available in misc section"""
  zip: str
  countryCode: str
  isResidence: NotRequired[bool]
  isDefaultAddress: NotRequired[bool]
  nationalityCountryCode: str

adapter = TypeAdapter(UserAddress)

class Create(Endpoint):
  async def create(
    self,
    user_address_body: UserAddressBody,
    *,
    validate: bool = True
  ) -> UserAddress:
    """Add address to an user
    
    - `user_address_body`: Address params
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/POST/v2/account/address)"""
    r = await self.authed_request(
      'POST', '/v2/account/address',
      json=user_address_body
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

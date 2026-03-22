from typing_extensions import NotRequired, TypedDict
from bit2me.types import UserAddress
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

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

adapter = TypeAdapter(list[UserAddress])

class Update(AuthEndpoint):
  async def update(
    self,
    user_address_body: UserAddressBody,
    *,
    address_id: str,
    validate: bool = True
  ) -> list[UserAddress]:
    """Update user address
    
    - `address_id`: The address id
    - `user_address_body`: Address params
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/PUT/v1/account/address)"""
    params: dict = {
      'addressId': address_id,
    }
    r = await self.authed_request(
      'put', '/v1/account/address',
      params=params,
    json=user_address_body
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

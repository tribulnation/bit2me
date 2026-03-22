from bit2me.types import UserAddress
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

adapter = TypeAdapter(list[UserAddress])

class List(AuthEndpoint):
  async def list(
    self,
    *,
    address_id: str | None = None,
    is_residence: bool | None = None,
    validate: bool = True
  ) -> list[UserAddress]:
    """Get the addresses of a specific user
    
    - `address_id`: The address id
    - `is_residence`: Value of the isResidence field
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/GET/v2/account/address)"""
    params = {}
    if address_id is not None:
      params['addressId'] = address_id
    if is_residence is not None:
      params['isResidence'] = is_residence
    r = await self.authed_request('GET', '/v2/account/address', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

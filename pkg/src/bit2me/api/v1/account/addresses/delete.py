from bit2me.core import AuthEndpoint

class Delete(AuthEndpoint):
  async def delete(self, *, address_id: str, validate: bool = True):
    """Remove user address
    
    - `address_id`: The address id
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/DELETE/v1/account/address)"""
    params: dict = {
      'addressId': address_id,
    }
    r = await self.authed_request('DELETE', '/v1/account/address', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return r.json()

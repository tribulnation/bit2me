from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

adapter = TypeAdapter(list[str])

class Conversion(AuthEndpoint):
  async def conversion(
    self,
    *,
    from_: str,
    to: str,
    value: str,
    time: str,
    validate: bool = True
  ) -> list[str]:
    """Convert the specified amounts to the specified currency
    
    - `from_`
    - `to`
    - `value`
    - `time`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/market/GET/v1/currency/convert)"""
    params: dict = {
      'from': from_,
      'to': to,
      'value': value,
      'time': time,
    }
    r = await self.authed_request('GET', '/v1/currency/convert', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

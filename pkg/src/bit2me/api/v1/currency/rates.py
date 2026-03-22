from typing_extensions import Any, Literal, TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class Entry(TypedDict):
  fiat: dict[str, Any]
  crypto: dict[str, Any]

adapter = TypeAdapter(list[Entry])

class Rates(AuthEndpoint):
  async def rates(
    self,
    *,
    type: Literal['all', 'fiat', 'crypto'] | None = None,
    time: str,
    validate: bool = True
  ) -> list[Entry]:
    """Return all supported exchange rates in USD.
    
    - `type`
    - `time`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/market/GET/v1/currency/rate)"""
    params: dict = {
      'time': time,
    }
    if type is not None:
      params['type'] = type
    r = await self.authed_request('GET', '/v1/currency/rate', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

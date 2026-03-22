from typing_extensions import TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class Extra(TypedDict):
  daily: float
  weekly: float
  monthly: float

adapter = TypeAdapter(dict[str, Extra])

class Apy(Endpoint):
  async def apy(self, *, validate: bool = True) -> dict[str, Extra]:
    """Get current annual percentage yields by currency. Value of currency is an object wich reward type as a key and annual percentage yield as value
    
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/earn/GET/v2/earn/apy)"""
    r = await self.request('GET', '/v2/earn/apy')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

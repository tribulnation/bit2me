from typing_extensions import TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class DataItem(TypedDict):
  id: str
  minimum: int
  maximum: int

class DepositEstimationResponse(TypedDict):
  total: int
  data: list[DataItem]

adapter = TypeAdapter(DepositEstimationResponse)

class DepositEstimations(Endpoint):
  async def __call__(self, *, validate: bool = True) -> DepositEstimationResponse:
    """Return all deposit estimates.
    
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/GET/v1/account/deposit-estimation)"""
    r = await self.authed_request('GET', '/v1/account/deposit-estimation')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

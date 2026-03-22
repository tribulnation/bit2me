from typing_extensions import TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class DataItem(TypedDict):
  id: str
  name: str
  description: str
  langCode: str

class ListPurposesResponse(TypedDict):
  total: int
  data: list[DataItem]

adapter = TypeAdapter(ListPurposesResponse)

class Purposes(Endpoint):
  async def __call__(
    self,
    *,
    lang_code: str | None = None,
    validate: bool = True
  ) -> ListPurposesResponse:
    """Return all purposes. Values are lowercase.
    
    - `lang_code`: Lang code
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/GET/v1/account/purposes)"""
    params = {}
    if lang_code is not None:
      params['langCode'] = lang_code
    r = await self.authed_request('GET', '/v1/account/purposes', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

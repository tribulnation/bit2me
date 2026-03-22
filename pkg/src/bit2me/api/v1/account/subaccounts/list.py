from typing_extensions import NotRequired, TypedDict
from bit2me.types import Phone
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class DataItem(TypedDict):
  id: NotRequired[str]
  email: NotRequired[str]
  name: NotRequired[str]
  surname: NotRequired[str]
  phone: NotRequired[Phone]

class ListSubaccountsResponse(TypedDict):
  total: NotRequired[float]
  data: NotRequired[list[DataItem]]

adapter = TypeAdapter(ListSubaccountsResponse)

class List(Endpoint):
  async def __call__(self, *, validate: bool = True) -> ListSubaccountsResponse:
    """Return the user's subaccounts.
    
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/GET/v1/account/subaccount)"""
    r = await self.authed_request('GET', '/v1/account/subaccount')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

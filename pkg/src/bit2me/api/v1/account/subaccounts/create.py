from typing_extensions import TypedDict
from bit2me.types import Phone
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class CreateSubaccountResponse(TypedDict):
  userId: str

class CreateSubaccountRequest(TypedDict):
  email: str
  name: str
  surname: str
  phone: Phone

adapter = TypeAdapter(CreateSubaccountResponse)

class Create(Endpoint):
  async def __call__(
    self,
    create_subaccount_request: CreateSubaccountRequest,
    *,
    validate: bool = True
  ) -> CreateSubaccountResponse:
    """Create a subaccount.
    
    - `create_subaccount_request`: The details to create the subaccount
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/POST/v1/account/subaccount)"""
    r = await self.authed_request(
      'POST', '/v1/account/subaccount',
      json=create_subaccount_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

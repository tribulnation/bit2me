from typing_extensions import TypedDict
from bit2me.types import BooleanResultResponse
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class EndSubaccountTwoFactorRequest(TypedDict):
  subaccountUserId: str
  totp: str

adapter = TypeAdapter(BooleanResultResponse)

class EnableFinish(Endpoint):
  async def enable_finish(
    self,
    end_subaccount_two_factor_request: EndSubaccountTwoFactorRequest,
    *,
    validate: bool = True
  ) -> BooleanResultResponse:
    """Finish the Google Authenticator 2FA enablement flow for a subaccount.
    
    - `end_subaccount_two_factor_request`: The details to end subaccount 2fa process
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/PUT/v1/account/subaccount/sfa)"""
    r = await self.authed_request(
      'put', '/v1/account/subaccount/sfa',
      json=end_subaccount_two_factor_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

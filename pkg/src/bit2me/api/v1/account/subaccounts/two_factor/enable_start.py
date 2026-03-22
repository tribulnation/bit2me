from typing_extensions import TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class InitSubaccountTwoFactorRequest(TypedDict):
  subaccountUserId: str

class InitSubaccountTwoFactorResponse(TypedDict):
  secret: str

adapter = TypeAdapter(InitSubaccountTwoFactorResponse)

class EnableStart(Endpoint):
  async def enable_start(
    self,
    init_subaccount_two_factor_request: InitSubaccountTwoFactorRequest,
    *,
    validate: bool = True
  ) -> InitSubaccountTwoFactorResponse:
    """Start the Google Authenticator 2FA enablement flow for a subaccount.
    
    - `init_subaccount_two_factor_request`: The details to init subaccount 2fa process
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/POST/v1/account/subaccount/sfa)"""
    r = await self.authed_request(
      'POST', '/v1/account/subaccount/sfa',
      json=init_subaccount_two_factor_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

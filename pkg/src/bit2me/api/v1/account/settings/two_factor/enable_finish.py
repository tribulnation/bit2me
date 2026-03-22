from typing_extensions import NotRequired, TypedDict
from bit2me.types import BooleanResultResponse
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class SettingsEnableTwoFactorEndRequest(TypedDict):
  totp: str
  sessionId: NotRequired[str]
  alwaysRequired: NotRequired[bool]

adapter = TypeAdapter(BooleanResultResponse)

class EnableFinish(AuthEndpoint):
  async def enable_finish(
    self,
    settings_enable_two_factor_end_request: SettingsEnableTwoFactorEndRequest,
    *,
    validate: bool = True
  ) -> BooleanResultResponse:
    """Finish the 2FA enablement flow by confirming that the client and server TOTP values match.
    
    - `settings_enable_two_factor_end_request`: The details to end the process
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/PUT/v1/account/settings/sfa)"""
    r = await self.authed_request(
      'put', '/v1/account/settings/sfa',
      json=settings_enable_two_factor_end_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

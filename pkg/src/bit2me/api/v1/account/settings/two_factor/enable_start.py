from typing_extensions import TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class SettingsEnableTwoFactorStartResponse(TypedDict):
  qrImage: str
  """QR image containing the otpauth URL for Google Authenticator (e.g. data:image/png;base64,iVB...YII=)"""
  secret: str
  """Shared secret key (base-32 encoded)"""
  name: str
  """The name to use with Google Authenticator"""

adapter = TypeAdapter(SettingsEnableTwoFactorStartResponse)

class EnableStart(AuthEndpoint):
  async def enable_start(
    self,
    *,
    validate: bool = True
  ) -> SettingsEnableTwoFactorStartResponse:
    """Start the 2FA enablement flow. After calling this endpoint, call `PUT /v1/account/settings/sfa` with a TOTP to finish the process.
    
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/POST/v1/account/settings/sfa)"""
    r = await self.authed_request('POST', '/v1/account/settings/sfa')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

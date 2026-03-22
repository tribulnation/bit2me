from typing_extensions import TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class IdentityVerificationRetryEligibilityResponse(TypedDict):
  result: bool

adapter = TypeAdapter(IdentityVerificationRetryEligibilityResponse)

class GetRetryWindow(AuthEndpoint):
  async def get_retry_window(
    self,
    *,
    validate: bool = True
  ) -> IdentityVerificationRetryEligibilityResponse:
    """Gets a response based on whether the user can retry the verification process
    
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/kyc/GET/v1/account/verify/identity/verification/retry)"""
    r = await self.authed_request(
      'GET', '/v1/account/verify/identity/verification/retry'
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

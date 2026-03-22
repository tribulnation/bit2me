from typing_extensions import Literal, NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class KycVerificationInitV3request(TypedDict):
  locale: str
  workflowId: NotRequired[float]
  """Workflow id: 10011"""
  successUrl: NotRequired[str]
  errorUrl: NotRequired[str]

class KycVerificationInitV3response(TypedDict):
  redirectUrl: NotRequired[str]
  token: NotRequired[str]
  reference: NotRequired[str]
  provider: NotRequired[Literal['jumio', 'incode']]

adapter = TypeAdapter(KycVerificationInitV3response)

class IdentityVerification(Endpoint):
  async def identity_verification(
    self,
    kyc_verification_init_v3request: KycVerificationInitV3request,
    *,
    validate: bool = True
  ) -> KycVerificationInitV3response:
    """Init KYC verification iframe.
    Open the redirectUrl in a native browser.
    
    Do NOT open the url in webviews to avoid incompatibilities with screen or camera recording permissions.
    
    - `kyc_verification_init_v3request`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/kyc/POST/v3/account/verify/identity/init)"""
    r = await self.authed_request(
      'POST', '/v3/account/verify/identity/init',
      json=kyc_verification_init_v3request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

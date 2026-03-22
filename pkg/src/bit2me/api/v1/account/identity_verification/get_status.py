from typing_extensions import Literal, NotRequired, TypedDict
from bit2me.types import PointsParam
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class ExtraMeasuresNotApproved(TypedDict):
  compliance: list[Literal['MR2']]

class KycExpress(TypedDict):
  status: NotRequired[Literal['success', 'rejected', 'uncompleted']]
  updatedAt: NotRequired[str]

class Risk(TypedDict):
  level: Literal['undefined', 'low', 'medium', 'high', 'unacceptable']
  minPoints: NotRequired[PointsParam]
  maxPoints: NotRequired[PointsParam]
  action: NotRequired[str]

class IdentityVerificationResponse(TypedDict):
  status: Literal['nodata', 'pending', 'verified', 'error']
  error: NotRequired[list[Literal['number', 'expiryDate', 'noDocUploaded', 'imageDoc', 'imageSelfie', 'other', 'unacceptableRisk', 'underAge', 'fraud', 'noNationality', 'idCountryDiffersResidenceCountry', 'kycUpdateRequired']]]
  image: list[Literal['document', 'selfie']]
  disableProcess: bool
  risk: NotRequired[Risk]
  kycExpress: NotRequired[KycExpress]
  questions: NotRequired[bool]
  extraMeasurePending: NotRequired[bool]
  extraMeasuresNotApproved: NotRequired[ExtraMeasuresNotApproved]
  tier: NotRequired[float]

adapter = TypeAdapter(IdentityVerificationResponse)

class GetStatus(Endpoint):
  async def get_status(self, *, validate: bool = True) -> IdentityVerificationResponse:
    """Return the current status of the identity verification
    
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/GET/v1/account/verify/identity)"""
    r = await self.authed_request('GET', '/v1/account/verify/identity')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

from typing_extensions import Literal, NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class CreateEarnMovementRequest(TypedDict):
  currency: str
  """Valid currency symbol"""
  amount: str
  type: Literal['deposit', 'withdrawal']
  lockPeriod: NotRequired[str]
  withholdingAmount: NotRequired[str]
  termsAndConditions: NotRequired[str]

class CreateEarnMovementResponse(TypedDict):
  walletMovementId: str
  movementId: str

adapter = TypeAdapter(CreateEarnMovementResponse)

class Create(AuthEndpoint):
  async def create(
    self,
    create_earn_movement_request: CreateEarnMovementRequest,
    *,
    validate: bool = True
  ) -> CreateEarnMovementResponse:
    """Create a deposit or withdrawal movement in Earn.
    
    - `create_earn_movement_request`: The details to create the movement
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/earn/POST/v1/earn/movements)"""
    r = await self.authed_request(
      'POST', '/v1/earn/movements',
      json=create_earn_movement_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

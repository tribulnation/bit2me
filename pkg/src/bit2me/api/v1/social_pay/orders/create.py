from typing_extensions import NotRequired, TypedDict
from bit2me.types import PayOrderData, PayOrderType, Phone
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class SocialPayOrderRequest(TypedDict):
  pocketId: str
  type: PayOrderType
  email: NotRequired[str]
  phone: NotRequired[Phone]
  alias: NotRequired[str]
  amount: str
  currency: str
  """Valid currency symbol"""
  note: NotRequired[str]

adapter = TypeAdapter(PayOrderData)

class Create(AuthEndpoint):
  async def create(
    self,
    social_pay_order_request: SocialPayOrderRequest,
    *,
    validate: bool = True
  ) -> PayOrderData:
    """Creates a new payment order
    
    - `social_pay_order_request`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/transfers/POST/v1/social-pay/order)"""
    r = await self.authed_request(
      'POST', '/v1/social-pay/order',
      json=social_pay_order_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

from typing_extensions import Any, Literal, NotRequired, TypedDict
from bit2me.types import TransactionSubsFeeTypeParam
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class Benefit(TypedDict):
  amount: str | float
  currency: str
  percentage: float
  tier: float
  levelId: NotRequired[str]

class Destination(TypedDict):
  type: Literal['pocket']
  value: str

class Method(TypedDict):
  type: Literal['creditcard', 'google-pay', 'apple-pay', 'hub-latam']
  params: NotRequired[dict[str, Any]]

class TellerCreateOrderProformaRequest(TypedDict):
  amount: str
  description: NotRequired[str]
  currency: str
  feeType: NotRequired[TransactionSubsFeeTypeParam]
  orderType: Literal['deposit', 'purchase']
  destination: NotRequired[Destination]
  method: Method

class TellerCreateOrderProformaResponse(TypedDict):
  orderId: str
  denomination: dict[str, Any]
  currency: str
  amountBeforeFee: str
  amountAfterFee: str
  fixedFee: str
  variableFee: str
  variableFeePercentage: str
  benefit: NotRequired[Benefit]

adapter = TypeAdapter(TellerCreateOrderProformaResponse)

class Preview(AuthEndpoint):
  async def preview(
    self,
    teller_create_order_proforma_request: TellerCreateOrderProformaRequest,
    *,
    validate: bool = True
  ) -> TellerCreateOrderProformaResponse:
    """Create a deposit proforma. To execute the resulting order, confirm it with `POST /v1/teller/order`.
    
    - `teller_create_order_proforma_request`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/funding/POST/v1/teller/order/proforma)"""
    r = await self.authed_request(
      'POST', '/v1/teller/order/proforma',
      json=teller_create_order_proforma_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

from typing_extensions import NotRequired, TypedDict
from bit2me.types import CreatedResourceIdResponse
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class ExecuteWalletTransactionRequest(TypedDict):
  proforma: str
  concept: NotRequired[str]
  note: NotRequired[str]

adapter = TypeAdapter(CreatedResourceIdResponse)

class Execute(Endpoint):
  async def execute(
    self,
    execute_wallet_transaction_request: ExecuteWalletTransactionRequest,
    *,
    validate: bool = True
  ) -> CreatedResourceIdResponse:
    """Executes a previuosly created transaction
    
    - `execute_wallet_transaction_request`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/wallet/POST/v1/wallet/transaction)"""
    r = await self.authed_request(
      'POST', '/v1/wallet/transaction',
      json=execute_wallet_transaction_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

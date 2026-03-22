from typing_extensions import TypedDict
from bit2me.types import BooleanResultResponse
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class UpdateTransactionRequest(TypedDict):
  note: str

adapter = TypeAdapter(BooleanResultResponse)

class Update(AuthEndpoint):
  async def update(
    self,
    id: str,
    update_transaction_request: UpdateTransactionRequest,
    *,
    validate: bool = True
  ) -> BooleanResultResponse:
    """Updates some data of the specified transaction
    
    - `id`: The transaction id
    - `update_transaction_request`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/wallet/PUT/v1/wallet/transaction/{id})"""
    r = await self.authed_request(
      'put', f'/v1/wallet/transaction/{id}',
      json=update_transaction_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

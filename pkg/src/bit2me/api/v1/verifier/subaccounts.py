from typing_extensions import Literal
from pydantic import TypeAdapter
from bit2me.core import Endpoint

adapter = TypeAdapter(str)

class Subaccounts(Endpoint):
  async def subaccounts(
    self,
    *,
    identity_file_type: Literal['backDocument', 'frontDocument', 'selfie', 'livenessFrontDocument', 'livenessBackDocument', 'livenessSelfie'],
    sub_account_id: str,
    validate: bool = True
  ) -> str:
    """Download an identity file of a subaccount
    
    - `identity_file_type`: The identity file type to download
    - `sub_account_id`: The identifier of the subaccount
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/kyc/GET/v1/verifier/subaccount/file)"""
    params: dict = {
      'identityFileType': identity_file_type,
      'subAccountId': sub_account_id,
    }
    r = await self.authed_request(
      'GET', '/v1/verifier/subaccount/file',
      params=params
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

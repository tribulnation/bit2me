from typing_extensions import NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class DataItem(TypedDict):
  id: NotRequired[str]
  name: NotRequired[str]
  description: NotRequired[str]
  langCode: NotRequired[str]

class ListEmploymentStatusesResponse(TypedDict):
  total: NotRequired[int]
  data: NotRequired[list[DataItem]]

adapter = TypeAdapter(ListEmploymentStatusesResponse)

class EmploymentStatuses(AuthEndpoint):
  async def __call__(
    self,
    *,
    lang_code: str | None = None,
    validate: bool = True
  ) -> ListEmploymentStatusesResponse:
    """Return all employment status translations. Values are lowercase.
    
    - `lang_code`: Lang code
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/GET/v1/account/employment-status)"""
    params = {}
    if lang_code is not None:
      params['langCode'] = lang_code
    r = await self.authed_request(
      'GET', '/v1/account/employment-status',
      params=params
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

from typing_extensions import Literal, NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class Entry(TypedDict):
  iso: str
  iso3: NotRequired[str]
  name: str
  fips: str
  """Federal Information Processing Standard  (https://en.wikipedia.org/wiki/Federal_Information_Processing_Standards)"""

adapter = TypeAdapter(list[Entry])

class Countries(AuthEndpoint):
  async def countries(
    self,
    country_isocode: str,
    *,
    lang_code: Literal['EN', 'ES'] | None = None,
    validate: bool = True
  ) -> list[Entry]:
    """Get country regions
    
    - `country_isocode`
    - `lang_code`: Language fo localize country names
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/misc/GET/v1/misc/country/{countryISOCode}/region)"""
    params = {}
    if lang_code is not None:
      params['langCode'] = lang_code
    r = await self.authed_request(
      'GET', f'/v1/misc/country/{country_isocode}/region',
      params=params
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

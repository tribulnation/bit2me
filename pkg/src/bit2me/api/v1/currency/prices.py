from typing_extensions import NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class Point(TypedDict):
  time: int
  interval: NotRequired[str]
  price: str

adapter = TypeAdapter(dict[str, list[Point]])

class Prices(AuthEndpoint):
  async def prices(
    self,
    *,
    currency: str | None = None,
    interval: list[str] | None = None,
    validate: bool = True
  ) -> dict[str, list[Point]]:
    """Return cryptocurrency prices in the selected currency across the requested intervals, including the current rate.
    
    - `currency`
    - `interval`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/market/GET/v1/currency/prices)"""
    params = {}
    if currency is not None:
      params['currency'] = currency
    if interval is not None:
      params['interval'] = interval
    r = await self.authed_request('GET', '/v1/currency/prices', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

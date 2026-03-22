from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

adapter = TypeAdapter(list[list[float | None]])

class Chart(AuthEndpoint):
  async def chart(
    self,
    *,
    ticker: str,
    temporality: list[str] | None = None,
    validate: bool = True
  ) -> list[list[float | None]]:
    """Returns historic price chart of given ticker
    
    - `ticker`
    - `temporality`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/market/GET/v3/currency/chart)"""
    params: dict = {
      'ticker': ticker,
    }
    if temporality is not None:
      params['temporality'] = temporality
    r = await self.authed_request('GET', '/v3/currency/chart', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

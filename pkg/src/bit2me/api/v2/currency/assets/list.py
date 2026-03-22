from typing_extensions import NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class Extra(TypedDict):
  symbol: str
  name: str
  slug: str
  mainwebUri: NotRequired[str]
  uriScheme: str
  hexColor: str
  assetType: str
  exponent: NotRequired[int]
  unitPriceScale: NotRequired[int]
  transactionUnitPriceScale: NotRequired[int]
  addressRegex: NotRequired[str]
  hasImage: bool
  hasPaymentRequest: bool
  isERC20Token: bool
  enabled: bool
  lite: NotRequired[bool]
  exchange: NotRequired[str]
  pairsWith: list[str]

adapter = TypeAdapter(dict[str, Extra])

class List(AuthEndpoint):
  async def list(
    self,
    *,
    include_testnet: bool | None = None,
    show_exchange: bool | None = None,
    validate: bool = True
  ) -> dict[str, Extra]:
    """Return all assets.
    
    - `include_testnet`
    - `show_exchange`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/market/GET/v2/currency/assets)"""
    params = {}
    if include_testnet is not None:
      params['includeTestnet'] = include_testnet
    if show_exchange is not None:
      params['showExchange'] = show_exchange
    r = await self.authed_request('GET', '/v2/currency/assets', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

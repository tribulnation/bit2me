from typing_extensions import NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class CurrencyAssetResponse(TypedDict):
  symbol: str
  name: str
  slug: str
  mainwebUri: str
  uriScheme: str
  hexColor: str
  assetType: str
  exponent: NotRequired[int]
  unitPriceScale: NotRequired[int]
  transactionUnitPriceScale: NotRequired[int]
  addressRegex: str
  hasImage: bool
  hasPaymentRequest: bool
  isERC20Token: bool
  enabled: bool
  lite: bool
  exchange: NotRequired[str]
  pairsWith: list[str]
  image: NotRequired[str]
  network: NotRequired[str]
  ticker: NotRequired[bool]
  loanable: NotRequired[bool]
  createdAt: NotRequired[str]
  highRisk: NotRequired[bool]
  stablecoin: NotRequired[bool]

adapter = TypeAdapter(CurrencyAssetResponse)

class Get(Endpoint):
  async def get(
    self,
    symbol: str,
    *,
    show_exchange: bool | None = None,
    validate: bool = True
  ) -> CurrencyAssetResponse:
    """Return an asset by symbol.
    
    - `symbol`
    - `show_exchange`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/market/GET/v2/currency/assets/{symbol})"""
    params = {}
    if show_exchange is not None:
      params['showExchange'] = show_exchange
    r = await self.authed_request(
      'GET', f'/v2/currency/assets/{symbol}',
      params=params
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

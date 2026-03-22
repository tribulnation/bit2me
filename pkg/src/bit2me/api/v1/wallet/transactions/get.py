from datetime import datetime
from typing_extensions import Literal, NotRequired, TypedDict
from bit2me.types import AmountCurrencyObject, Rate, TransactionSubsFeeTypeParam
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class Flip(TypedDict):
  percentage: str
  amount: str
  currency: str
  """Valid currency symbol"""

class Teller(TypedDict):
  id: NotRequired[str]
  """Teller orderId"""
  feeCurrency: NotRequired[str]
  """Currency of the fees"""
  fixedFee: NotRequired[str]
  """Fixed fee"""
  variableFee: NotRequired[str]
  """Variable fee"""
  variableFeePercentage: NotRequired[str]
  """Variable fee percentage"""

class Transaction(TypedDict):
  """Network transaction"""
  hash: str
  """Network transaction hash"""
  confirmedAt: NotRequired[datetime]
  """When the transaction was confirmed (ISO 8601)."""
  confirmationCount: NotRequired[float]
  """The number of confirmations the transaction has."""

DestinationKeywords = TypedDict('DestinationKeywords', {'class': Literal['pocket', 'network', 'b2m', 'bankAccount']})
"""
  - `class`:   Type of the destination:
     - pocket: destination is another pocket
     - network: destination is an cryptocurrency address
     - b2m: destination is another Bit2Me user
     - bankAccount: destination is a bank account
    
"""

class Destination(DestinationKeywords):
  """Transaction destination"""
  currency: str
  """The currency of the destination"""
  amount: str
  """The total amount of "money" that the destination receives"""
  pocketName: NotRequired[str]
  """The destination pocket name"""
  pocketId: NotRequired[str]
  """The destination pocket ID"""
  address: NotRequired[str | None]
  """The destination address"""
  addressNetwork: NotRequired[str | None]
  """The destination address network"""
  addressInBlacklist: NotRequired[bool | None]
  """Indicates if destination address is in blacklist"""
  addressTag: NotRequired[str | None]
  rate: NotRequired[Rate]

class Fee(TypedDict):
  """Different fees for the transaction:
  network: only present when type is "withdrawal"
  flip: only present when the transaction has a currency convertion (instant)"""
  network: NotRequired[AmountCurrencyObject]
  flip: NotRequired[Flip]
  teller: NotRequired[Teller]

OriginKeywords = TypedDict('OriginKeywords', {'class': Literal['pocket', 'network', 'b2m', 'card', 'bank transfer', 'trading']})
"""
  - `class`:   Type of the origin:
     - pocket: origin is another pocket
     - network: origin is a cryptocurrency address
     - b2m: origin is another Bit2Me user
     - card: origin is a credit or debit card
     - bank transfer: origin is a bank transfer
     - trading: origin is trading balance
    
"""

class Origin(OriginKeywords):
  """Transaction origin"""
  currency: str
  """The origin currency"""
  amount: str
  """The total amount of "money" that is taken from origin."""
  pocketName: NotRequired[str | None]
  """The origin pocket name"""
  pocketId: NotRequired[str | None]
  """The origin pocket ID"""
  rate: NotRequired[Rate]

class WalletTransactionDetailResponse(TypedDict):
  date: datetime
  """When the transaction was created (ISO 8601)"""
  type: Literal['deposit', 'withdrawal', 'transfer']
  """Type of the transaction"""
  concept: NotRequired[str | None]
  """The concept of the transaction"""
  note: NotRequired[str | None]
  """Personal note of the user"""
  origin: Origin
  destination: Destination
  transaction: NotRequired[Transaction]
  fee: NotRequired[Fee]
  flip: NotRequired[Rate]
  substractFeeType: NotRequired[TransactionSubsFeeTypeParam | None]

adapter = TypeAdapter(WalletTransactionDetailResponse)

class Get(Endpoint):
  async def get(
    self,
    id: str,
    *,
    user_currency: str | None = None,
    validate: bool = True
  ) -> WalletTransactionDetailResponse:
    """Get the details of a transaction
    
    - `id`: The transaction id (returned by GET /v1/transaction)
    - `user_currency`: The user's currency (used to show a rate from it to Euro)
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/wallet/GET/v1/wallet/transaction/{id})"""
    params = {}
    if user_currency is not None:
      params['userCurrency'] = user_currency
    r = await self.authed_request(
      'GET', f'/v1/wallet/transaction/{id}',
      params=params
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

from datetime import datetime
from typing_extensions import Any, Literal, NotRequired, TypedDict
from bit2me.types import (
  AmountCurrencyObject,
  Phone,
  Rate,
  TransactionSubsFeeTypeParam
)
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class BankAccount(TypedDict):
  bankAccount: str
  swiftBic: NotRequired[str]
  country: str
  receiverName: NotRequired[str]
  bankName: NotRequired[str]
  bankAddress: NotRequired[str]
  bankCode: NotRequired[str]
  bankBranch: NotRequired[str]

class Creditcard(TypedDict):
  cardId: str

class Fixed(TypedDict):
  amount: str
  currency: str
  """Valid currency symbol"""

class Flip(TypedDict):
  """Flip fee"""
  percentage: str
  amount: str
  currency: str
  """Valid currency symbol"""

class Network(TypedDict):
  """Network fee"""
  amount: str
  currency: str

class UserAmount(TypedDict):
  currency: str
  """Valid currency symbol"""
  amount: str

class Variable(TypedDict):
  percentage: str
  amount: str
  currency: str
  """Valid currency symbol"""

class Destination(TypedDict):
  address: NotRequired[str]
  pocket: NotRequired[str]
  bankAccount: NotRequired[BankAccount]
  email: NotRequired[str]
  phone: NotRequired[Phone]
  alias: NotRequired[str]
  network: NotRequired[str]
  """The destination address network"""

class Origin(TypedDict):
  creditcard: NotRequired[Creditcard]

class Teller(TypedDict):
  fixed: Fixed
  variable: Variable

class Fee(TypedDict):
  """Different fees for the transaction"""
  network: NotRequired[Network]
  flip: NotRequired[Flip]
  teller: NotRequired[Teller]

class WalletTransactionProformaRequest(TypedDict):
  operation: NotRequired[Literal['purchase', 'withdrawal-trading', 'deposit-trading', 'social-payment', 'launchpad-purchase', 'buy', 'sell']]
  """This property is not necessary for other operation types"""
  pair: NotRequired[str]
  pocket: NotRequired[str]
  amount: str
  currency: str
  type: NotRequired[TransactionSubsFeeTypeParam]
  concept: NotRequired[str]
  note: NotRequired[str]
  receiverName: NotRequired[str]
  origin: NotRequired[Origin]
  destination: NotRequired[Destination]
  userCurrency: NotRequired[str]
  """The user's currency (used to show a rate from it to Euro)"""
  queryParams: NotRequired[dict[str, Any]]
  """Used for some cryptos that need extra parameters to do blockchain sendings. For example, memo in XRP."""

class WalletTransactionProformaResponse(TypedDict):
  id: str
  expirationTime: datetime
  origin: AmountCurrencyObject
  destination: AmountCurrencyObject
  fee: NotRequired[Fee]
  flip: NotRequired[Rate]
  userRate: NotRequired[Rate]
  userAmount: NotRequired[UserAmount]

adapter = TypeAdapter(WalletTransactionProformaResponse)

class Preview(Endpoint):
  async def preview(
    self,
    wallet_transaction_proforma_request: WalletTransactionProformaRequest,
    *,
    validate: bool = True
  ) -> WalletTransactionProformaResponse:
    """Create a new proforma transaction, including its expiration time.
    
    - If `type` is not specified, `REA` is used by default.
    - `destination` only accepts one field. Use `destination.address` for a cryptocurrency address or `destination.pocket` for the destination pocket ID.
    - The user's email must be validated before calling this endpoint.
    - For peer-to-peer transactions, a sell operation must be made on the source pocket and a buy operation must be made on the destination pocket.
    - All blockchain withdrawals must include Travel Rule information before they can be processed. See `POST /v1/blockchain-manager/travel-rule-order/{orderId}`.
    
    - `wallet_transaction_proforma_request`
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/wallet/POST/v1/wallet/transaction/proforma)"""
    r = await self.authed_request(
      'POST', '/v1/wallet/transaction/proforma',
      json=wallet_transaction_proforma_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

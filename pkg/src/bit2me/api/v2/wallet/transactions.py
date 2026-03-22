from datetime import datetime
from typing_extensions import Literal, NotRequired, TypedDict
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class Benefit(TypedDict):
  tier: NotRequired[int]
  levelId: NotRequired[str]
  quantity: NotRequired[str]
  percentage: NotRequired[int]
  currency: NotRequired[str]
  amount: NotRequired[float]

class Converted(TypedDict):
  amount: NotRequired[str]
  amountAfterFees: NotRequired[str]
  currency: NotRequired[str]

class Converted2(TypedDict):
  amount: NotRequired[str]
  amountAfterFees: NotRequired[str]
  currency: NotRequired[str]

class Fixed(TypedDict):
  amount: NotRequired[str]
  currency: NotRequired[str]

class Flip(TypedDict):
  percentage: NotRequired[str]
  amount: NotRequired[str]
  currency: NotRequired[str]

class Network(TypedDict):
  amount: NotRequired[str]
  currency: NotRequired[str]

class Pair(TypedDict):
  base: NotRequired[str]
  quote: NotRequired[str]

class Pair2(TypedDict):
  base: NotRequired[str]
  quote: NotRequired[str]

class Pair3(TypedDict):
  base: NotRequired[str]
  quote: NotRequired[str]

class Pair4(TypedDict):
  base: NotRequired[str]
  quote: NotRequired[str]

class Pair5(TypedDict):
  base: NotRequired[str]
  quote: NotRequired[str]

class Pair6(TypedDict):
  base: NotRequired[str]
  quote: NotRequired[str]

class Phone2(TypedDict):
  number: NotRequired[str]
  countryCode: NotRequired[str]

class Phone3(TypedDict):
  number: NotRequired[str]
  countryCode: NotRequired[str]

class Transaction(TypedDict):
  hash: NotRequired[str]
  confirmedAt: NotRequired[str]
  confirmationCount: NotRequired[int]

class UserAmount(TypedDict):
  currency: NotRequired[str]
  value: NotRequired[str]

class UserAmount2(TypedDict):
  currency: NotRequired[str]
  value: NotRequired[str]

class UserAmount3(TypedDict):
  currency: NotRequired[str]
  amount: NotRequired[str]

class Variable(TypedDict):
  percentage: NotRequired[str]
  amount: NotRequired[str]
  currency: NotRequired[str]

class Rate10(TypedDict):
  value: NotRequired[str]
  pair: NotRequired[Pair6]

class Rate3(TypedDict):
  value: NotRequired[str]
  pair: NotRequired[Pair]

class Rate5(TypedDict):
  value: NotRequired[str]
  pair: NotRequired[Pair2]

class Rate7(TypedDict):
  value: NotRequired[str]
  pair: NotRequired[Pair3]

class Rate8(TypedDict):
  value: NotRequired[str]
  pair: NotRequired[Pair4]

class Rate9(TypedDict):
  value: NotRequired[str]
  pair: NotRequired[Pair5]

class Teller(TypedDict):
  fixed: NotRequired[Fixed]
  variable: NotRequired[Variable]
  id: NotRequired[str]
  feeCurrency: NotRequired[str]
  fixedFee: NotRequired[str]
  variableFee: NotRequired[str]
  variableFeePercentage: NotRequired[str]

class Destination2(TypedDict):
  currency: NotRequired[str]
  amount: NotRequired[str]
  rate: NotRequired[Rate10]

class Fee(TypedDict):
  network: NotRequired[Network]
  flip: NotRequired[Flip]
  teller: NotRequired[Teller]

class Flip2(TypedDict):
  rate: NotRequired[Rate8]

class Rate2(TypedDict):
  rate: NotRequired[Rate3]

class Rate4(TypedDict):
  rate: NotRequired[Rate5]

class Rate6(TypedDict):
  rate: NotRequired[Rate7]

class UserRate(TypedDict):
  rate: NotRequired[Rate9]

class Company(TypedDict):
  destination: NotRequired[Destination2]

class Denomination(TypedDict):
  amount: NotRequired[str]
  currency: NotRequired[str]
  rate: NotRequired[Rate2]

DestinationKeywords = TypedDict('DestinationKeywords', {'class': str})

class Destination(DestinationKeywords):
  currency: NotRequired[str]
  pocketName: NotRequired[str | None]
  pocketId: NotRequired[str | None]
  bankAccount: NotRequired[str]
  email: NotRequired[str]
  phone: NotRequired[Phone3]
  alias: NotRequired[str]
  fullName: NotRequired[str]
  address: NotRequired[str | None]
  addressNetwork: NotRequired[str | None]
  addressTag: NotRequired[str | None]
  addressInBlacklist: NotRequired[bool | None]
  amount: NotRequired[str]
  amountAfterFees: NotRequired[str]
  rate: NotRequired[Rate6]
  converted: NotRequired[Converted2]
  userAmount: NotRequired[UserAmount2]
  userId: NotRequired[str]

OriginKeywords = TypedDict('OriginKeywords', {'class': str})

class Origin(OriginKeywords):
  currency: NotRequired[str]
  pocketName: NotRequired[str | None]
  pocketId: NotRequired[str | None]
  bankAccount: NotRequired[str]
  email: NotRequired[str]
  phone: NotRequired[Phone2]
  alias: NotRequired[str]
  fullName: NotRequired[str]
  address: NotRequired[str | None]
  addressNetwork: NotRequired[str | None]
  addressTag: NotRequired[str | None]
  addressInBlacklist: NotRequired[bool | None]
  amount: NotRequired[str]
  amountAfterFees: NotRequired[str]
  rate: NotRequired[Rate4]
  converted: NotRequired[Converted]
  userAmount: NotRequired[UserAmount]
  userId: NotRequired[str]

class DataItem(TypedDict):
  id: NotRequired[str]
  note: NotRequired[str]
  date: NotRequired[datetime]
  completedAt: NotRequired[datetime]
  canceledAt: NotRequired[datetime | None]
  concept: NotRequired[str]
  type: NotRequired[str]
  subtype: NotRequired[str]
  method: NotRequired[str]
  status: NotRequired[str]
  substractFeeType: NotRequired[str]
  denomination: NotRequired[Denomination]
  frequency: NotRequired[str]
  isInitialRecurringOrder: NotRequired[bool]
  origin: NotRequired[Origin]
  destination: NotRequired[Destination]
  transaction: NotRequired[Transaction]
  fee: NotRequired[Fee]
  flip: NotRequired[Flip2]
  benefit: NotRequired[Benefit]
  userRate: NotRequired[UserRate]
  userAmount: NotRequired[UserAmount3]
  instantId: NotRequired[str]
  company: NotRequired[Company]

class ListWalletTransactionsV2response(TypedDict):
  data: NotRequired[list[DataItem]]
  total: NotRequired[int]

adapter = TypeAdapter(ListWalletTransactionsV2response)

class Transactions(Endpoint):
  async def transactions(
    self,
    *,
    offset: int | None = None,
    limit: int | None = None,
    year: int | None = None,
    currency: str | None = None,
    operation: Literal['purchase', 'sell', 'swap', 'deposit', 'withdrawal', 'deposit-earn', 'withdrawal-earn', 'deposit-trading', 'withdrawal-trading', 'send-pay', 'receive-pay', 'purchase-bcard', 'reimburse-bcard', 'send', 'receive'] | None = None,
    validate: bool = True
  ) -> ListWalletTransactionsV2response:
    """Get user transactions.
    Transactions can be paginated using **offset** and **limit** parameters. For example, to get the third page and show 20 registers per page you would use the following query:
    
    ``` /v2/wallet/transaction?offset=40&limit=20 ```
    
    - `offset`: Specify the number of entries to be skipped (0 by default)
    - `limit`: Specify the maximum number of entries to be returned (20 by default)
    - `year`: Filter movements to this specific year
    - `currency`: Currency in which movements has been involved
    - `operation`: Operation to filter
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/wallet/GET/v2/wallet/transaction)"""
    params = {}
    if offset is not None:
      params['offset'] = offset
    if limit is not None:
      params['limit'] = limit
    if year is not None:
      params['year'] = year
    if currency is not None:
      params['currency'] = currency
    if operation is not None:
      params['operation'] = operation
    r = await self.authed_request('GET', '/v2/wallet/transaction', params=params)
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

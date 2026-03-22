from datetime import datetime
from typing_extensions import Literal, NotRequired, TypedDict
from bit2me.types import (
  BooleanResultResponse,
  DepositEstimation,
  FundsOrigin,
  UserType
)
from pydantic import TypeAdapter
from bit2me.core import AuthEndpoint

class Address(TypedDict):
  country: str
  """The 2-letter country code"""
  state: str
  city: str
  street: str
  zip: str

class Identity(TypedDict):
  type: NotRequired[Literal['idcard', 'passport', 'drivinglicense', 'visa']]
  number: NotRequired[str]
  expiryDate: NotRequired[datetime]
  countryCode: NotRequired[str]

class Profile(TypedDict):
  langCode: NotRequired[str]
  currencyCode: NotRequired[str]
  timeZone: NotRequired[str]

class Person(TypedDict):
  name: NotRequired[str]
  surname: NotRequired[str]
  gender: NotRequired[Literal['male', 'female', 'N/D']]
  birthDate: NotRequired[datetime]
  nationalityCountryCode: NotRequired[str]
  employmentStatus: NotRequired[Literal['employed', 'student', 'selfEmployed', 'retired', 'unemployed']]
  profession: NotRequired[str]
  identity: NotRequired[Identity]

class UpdateAccountRequest(TypedDict):
  alias: NotRequired[str]
  person: NotRequired[Person]
  profile: NotRequired[Profile]
  address: NotRequired[Address]
  depositEstimation: NotRequired[DepositEstimation]
  selfInvoiceIdentityNumber: NotRequired[str]
  fundsOrigin: NotRequired[FundsOrigin]
  type: NotRequired[UserType]
  so: NotRequired[str]
  version: NotRequired[str]

adapter = TypeAdapter(BooleanResultResponse)

class Update(AuthEndpoint):
  async def __call__(
    self,
    update_account_request: UpdateAccountRequest,
    *,
    validate: bool = True
  ) -> BooleanResultResponse:
    """Update account information.
    
    - `update_account_request`: The account details to be updated
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/PUT/v1/account/update)"""
    r = await self.authed_request(
      'put', '/v1/account/update',
      json=update_account_request
    )
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

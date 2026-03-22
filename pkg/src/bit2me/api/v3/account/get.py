from datetime import datetime
from typing_extensions import Literal, NotRequired, TypedDict
from bit2me.types import DepositEstimation, FundsOrigin, Phone, UserType
from pydantic import TypeAdapter
from bit2me.core import Endpoint

class AttorneyInFact(TypedDict):
  name: NotRequired[str]
  surname: NotRequired[str]
  typeOfDocument: NotRequired[Literal['none', 'idcard', 'foreign-id-card', 'passport', 'drivinglicense', 'visa']]
  numberOfDocument: NotRequired[str]

class Avatar(TypedDict):
  sm: NotRequired[str]
  md: NotRequired[str]
  lg: NotRequired[str]

class Contact(TypedDict):
  name: NotRequired[str]
  surname: NotRequired[str]
  typeOfDocument: NotRequired[Literal['none', 'idcard', 'foreign-id-card', 'passport', 'drivinglicense', 'visa']]
  numberOfDocument: NotRequired[str]

class Identity(TypedDict):
  type: NotRequired[Literal['none', 'idcard', 'passport', 'drivinglicense', 'visa', 'cif']]
  number: NotRequired[str]
  countryCode: NotRequired[str]
  updatedAt: NotRequired[datetime]

class PartnersItem(TypedDict):
  nationalityCountryCode: NotRequired[str]
  companyPartnerId: str
  documentType: NotRequired[Literal['none', 'idcard', 'foreign-id-card', 'passport', 'drivinglicense', 'visa']]
  documentNumber: NotRequired[str]
  documentCountryCode: NotRequired[str]
  birthdate: NotRequired[datetime]
  sharePercentage: NotRequired[float]
  fullName: NotRequired[str]
  isPoliticallyExposed: NotRequired[bool]
  deletedAt: NotRequired[datetime]

class Person(TypedDict):
  name: NotRequired[str]
  surname: NotRequired[str]
  gender: NotRequired[Literal['male', 'female', 'N/D']]
  nationalityCountryCode: NotRequired[str]

class PoliticalPartnersItem(TypedDict):
  name: NotRequired[str]
  position: NotRequired[str]

class SecondFactorAuth(TypedDict):
  alwaysRequired: NotRequired[bool]

class Company(TypedDict):
  businessName: NotRequired[str]
  kindOfSociety: NotRequired[str]
  constitutionDate: NotRequired[datetime]
  constitutionCountryCode: NotRequired[str]
  registeredOffice: NotRequired[str]
  sector: NotRequired[str]
  autonomus: NotRequired[bool]
  obligedSubject: NotRequired[bool]
  overTheCounter: NotRequired[bool]
  politicallyExposedPersonPartners: NotRequired[bool]
  politicalPartners: NotRequired[list[PoliticalPartnersItem]]
  firstTradeEstimatedValue: NotRequired[int]
  annualTradeEstimatedValue: NotRequired[int]
  billingVolume: NotRequired[int]
  numberOfPartners: NotRequired[int]
  reasonForTheOperation: NotRequired[list[str]]
  typeOfOperationsToPerform: NotRequired[list[str]]
  identity: NotRequired[Identity]
  taxId: NotRequired[str]
  legalEntityId: NotRequired[str]
  contact: NotRequired[Contact]
  attorneyInFact: NotRequired[AttorneyInFact]
  legalTerms: NotRequired[bool]
  service: NotRequired[str]
  webUrl: NotRequired[str | None]
  shareholdingStructure: NotRequired[str | None]
  services: NotRequired[list[Literal['crypto_investment', 'send_crypto', 'liquidity', 'earn_loan', 'api', 'consulting', 'other']]]
  otherServices: NotRequired[str | None]
  partners: NotRequired[list[PartnersItem]]
  economicCapacityModel: NotRequired[Literal['model_200', 'model_390', 'model_303']]

class Profile(TypedDict):
  langCode: NotRequired[str]
  currencyCode: NotRequired[str]
  timeZone: NotRequired[str]
  avatar: NotRequired[Avatar]

class AccountDetailsV3response(TypedDict):
  id: str
  email: str
  realEmail: NotRequired[str]
  phone: NotRequired[Phone]
  alias: NotRequired[str]
  person: NotRequired[Person]
  profile: NotRequired[Profile]
  selfInvoiceIdentityNumber: NotRequired[str]
  registrationDate: NotRequired[datetime]
  type: NotRequired[UserType]
  depositEstimation: NotRequired[DepositEstimation]
  fundsOrigin: NotRequired[FundsOrigin]
  accountPurpose: NotRequired[Literal['savings', 'currencyExchange', 'investment', 'trading', 'cryptocurrencyPayments']]
  secondFactorAuth: NotRequired[SecondFactorAuth]
  documentValidity: NotRequired[Literal['valid', 'almostExpired', 'expired', 'updateRequired']]
  company: NotRequired[Company]
  accountCompleted: NotRequired[bool]
  knowledgeLevel: NotRequired[float]
  registrationReason: NotRequired[Literal['investing', 'diversification', 'savings', 'curiosity', 'blockchain']]
  knowledgeQuestionsStatus: NotRequired[Literal['completed', 'uncompleted', 'omitted']]

adapter = TypeAdapter(AccountDetailsV3response)

class Get(Endpoint):
  async def get(self, *, validate: bool = True) -> AccountDetailsV3response:
    """Get account details, personal data is returned masked
    
    - `validate`: Whether to validate the response against the expected schema (default: True) (default: None)
    
    [Official docs](https://api.bit2me.com/doc#tag/account/GET/v3/account)"""
    r = await self.authed_request('GET', '/v3/account')
    
    if r.status_code != 200:
      self.raise_error(r)
    return adapter.validate_json(r.text) if self.should_validate(validate) else r.json()

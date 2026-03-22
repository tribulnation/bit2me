from bit2me.core.mixin import Router
from .addresses import Addresses
from .delete import Delete
from .deposit_estimations import DepositEstimations
from .employment_statuses import EmploymentStatuses
from .funds_origins import FundsOrigins
from .identity_verification import IdentityVerification
from .person_identity import PersonIdentity
from .professions import Professions
from .purposes import Purposes
from .settings import Settings
from .subaccounts import Subaccounts
from .update import Update

class Account(Router):
  addresses: Addresses
  delete: Delete
  deposit_estimations: DepositEstimations
  employment_statuses: EmploymentStatuses
  funds_origins: FundsOrigins
  identity_verification: IdentityVerification
  person_identity: PersonIdentity
  professions: Professions
  purposes: Purposes
  settings: Settings
  subaccounts: Subaccounts
  update: Update

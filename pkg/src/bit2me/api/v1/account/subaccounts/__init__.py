from bit2me.core.mixin import Router
from .create import Create
from .list import List
from .two_factor import TwoFactor

class Subaccounts(Router):
  create: Create
  list: List
  two_factor: TwoFactor

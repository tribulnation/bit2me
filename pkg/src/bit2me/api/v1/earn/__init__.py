from bit2me.core.mixin import Router
from .movements import Movements
from .summary import Summary
from .wallets import Wallets

class Earn(Router):
  movements: Movements
  summary: Summary
  wallets: Wallets

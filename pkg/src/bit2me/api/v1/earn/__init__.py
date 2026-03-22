from bit2me.core.mixin import AuthRouter
from .movements import Movements
from .summary import Summary
from .wallets import Wallets

class Earn(AuthRouter):
  movements: Movements
  summary: Summary
  wallets: Wallets

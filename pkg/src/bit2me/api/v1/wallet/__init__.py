from bit2me.core.mixin import Router
from .pockets import Pockets
from .settings import Settings
from .transactions import Transactions

class Wallet(Router):
  pockets: Pockets
  settings: Settings
  transactions: Transactions

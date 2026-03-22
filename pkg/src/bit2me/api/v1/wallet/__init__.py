from bit2me.core.mixin import AuthRouter
from .pockets import Pockets
from .settings import Settings
from .transactions import Transactions

class Wallet(AuthRouter):
  pockets: Pockets
  settings: Settings
  transactions: Transactions

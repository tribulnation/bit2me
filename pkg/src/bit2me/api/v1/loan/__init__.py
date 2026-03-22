from bit2me.core.mixin import AuthRouter
from .ltv import Ltv
from .movements import Movements
from .orders import Orders

class Loan(AuthRouter):
  ltv: Ltv
  movements: Movements
  orders: Orders

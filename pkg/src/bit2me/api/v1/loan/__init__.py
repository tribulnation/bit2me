from bit2me.core.mixin import Router
from .ltv import Ltv
from .movements import Movements
from .orders import Orders

class Loan(Router):
  ltv: Ltv
  movements: Movements
  orders: Orders

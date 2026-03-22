from bit2me.core.mixin import Router
from .ibans import Ibans
from .orders import Orders
from .pockets import Pockets

class Teller(Router):
  ibans: Ibans
  orders: Orders
  pockets: Pockets

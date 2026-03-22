from bit2me.core.mixin import AuthRouter
from .ibans import Ibans
from .orders import Orders
from .pockets import Pockets

class Teller(AuthRouter):
  ibans: Ibans
  orders: Orders
  pockets: Pockets

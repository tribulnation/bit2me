from bit2me.core.mixin import AuthRouter
from .orders import Orders

class SocialPay(AuthRouter):
  orders: Orders

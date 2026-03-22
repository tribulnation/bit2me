from bit2me.core.mixin import Router
from .orders import Orders

class SocialPay(Router):
  orders: Orders

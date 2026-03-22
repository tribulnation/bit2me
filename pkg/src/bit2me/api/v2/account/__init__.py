from bit2me.core.mixin import AuthRouter
from .addresses import Addresses

class Account(AuthRouter):
  addresses: Addresses

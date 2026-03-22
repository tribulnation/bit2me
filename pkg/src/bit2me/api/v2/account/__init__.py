from bit2me.core.mixin import Router
from .addresses import Addresses

class Account(Router):
  addresses: Addresses

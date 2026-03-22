from bit2me.core.mixin import Router
from .account import Account
from .currency import Currency
from .signin import Signin

class V3(Router):
  account: Account
  currency: Currency
  signin: Signin

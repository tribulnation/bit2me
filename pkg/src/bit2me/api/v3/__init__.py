from bit2me.core.mixin import AuthRouter
from .account import Account
from .currency import Currency
from .signin import Signin

class V3(AuthRouter):
  account: Account
  currency: Currency
  signin: Signin

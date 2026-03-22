from bit2me.core.mixin import AuthRouter
from .account import Account
from .currency import Currency
from .earn import Earn
from .loan import Loan
from .trading import Trading
from .wallet import Wallet

class V2(AuthRouter):
  account: Account
  currency: Currency
  earn: Earn
  loan: Loan
  trading: Trading
  wallet: Wallet

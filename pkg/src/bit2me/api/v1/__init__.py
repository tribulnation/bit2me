from bit2me.core.mixin import AuthRouter
from .account import Account
from .blockchain_manager import BlockchainManager
from .currency import Currency
from .earn import Earn
from .loan import Loan
from .misc import Misc
from .signin import Signin
from .social_pay import SocialPay
from .teller import Teller
from .trading import Trading
from .verifier import Verifier
from .wallet import Wallet

class V1(AuthRouter):
  account: Account
  blockchain_manager: BlockchainManager
  currency: Currency
  earn: Earn
  loan: Loan
  misc: Misc
  signin: Signin
  social_pay: SocialPay
  teller: Teller
  trading: Trading
  verifier: Verifier
  wallet: Wallet

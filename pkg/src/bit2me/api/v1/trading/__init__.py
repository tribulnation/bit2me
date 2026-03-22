from bit2me.core.mixin import Router
from .balance import Balance
from .candles import Candles
from .funding_movements import FundingMovements
from .markets import Markets
from .orders import Orders
from .trades import Trades
from .wallets import Wallets

class Trading(Router):
  balance: Balance
  candles: Candles
  funding_movements: FundingMovements
  markets: Markets
  orders: Orders
  trades: Trades
  wallets: Wallets

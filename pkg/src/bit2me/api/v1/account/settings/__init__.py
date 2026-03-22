from bit2me.core.mixin import Router
from .two_factor import TwoFactor

class Settings(Router):
  two_factor: TwoFactor

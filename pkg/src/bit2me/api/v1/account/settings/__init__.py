from bit2me.core.mixin import AuthRouter
from .two_factor import TwoFactor

class Settings(AuthRouter):
  two_factor: TwoFactor

from bit2me.core.mixin import AuthRouter
from .assets import Assets

class Currency(AuthRouter):
  assets: Assets

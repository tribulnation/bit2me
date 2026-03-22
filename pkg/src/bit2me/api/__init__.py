from bit2me.core.mixin import Router
from .v1 import V1
from .v2 import V2
from .v3 import V3

class Bit2Me(Router):
  v1: V1
  v2: V2
  v3: V3

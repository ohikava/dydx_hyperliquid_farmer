from dydx_hyperliquid_farmer.dydx import DyDx
from dydx_hyperliquid_farmer.hyperliquid import HyperLiquid

class FarmingBot:
    def __init__(self) -> None:
        self.dydx = DyDx()
        self.hyperliquid = HyperLiquid()
        print('IMPORTED CORRECTLY')


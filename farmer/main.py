from farmer.dydx import DyDx
from farmer.hyperliquid import HyperLiquid

class FarmingBot:
    def __init__(self) -> None:
        self.dydx = DyDx()
        self.hyperliquid = HyperLiquid()
        print('IMPORTED CORRECTLY')


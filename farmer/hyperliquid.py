from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from hyperliquid.utils.constants import TESTNET_API_URL, MAINNET_API_URL
from farmer.utils import handle_order_execution_results_hl
import eth_account
import logging 
from typing import Optional


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class HyperLiquid:
    DEFAULT_SLIPPAGE = 0.05

    def __init__(self, mainnet=True, create_acc=False) -> None:
        
        if create_acc:
            self.generate_account()
        else:
            self.get_account()
        
        print(self.address)

        if mainnet:
            self.info = Info(MAINNET_API_URL, skip_ws=True)
            self.exchange = Exchange(self.account, MAINNET_API_URL)
        else:
            self.info = Info(TESTNET_API_URL, skip_ws=True)
            self.exchange = Exchange(self.account, TESTNET_API_URL)
    
    def get_acc_info(self):
        return self.info.user_state(self.address)

    def generate_account(self):
        """
        Function generates an ETH accoun and saves its private key into the file
        """
        acc = eth_account.Account.create()
        self.account = acc 
        self.address = acc.address
        self.private_key = acc._private_key.hex()

        logger.info(f"Current public key: {self.address}, Current private key: {self.private_key}")
        
        with open("hyperliquid_pk.txt", 'a') as f:
            f.write(self.private_key + "\n")

    def get_account(self):
        """
        Loads an ETH account from the file with private key
        """
        with open("hyperliquid_pk.txt", 'r') as f:
            self.private_key = f.readline().strip()

        self.account = eth_account.Account.from_key(self.private_key)
        self.address = self.account.address

        logger.info(f"Current public key: {self.address}, Current private key: {self.private_key}")

    def get_account_balance(self):
        pass

    def _market_order(self, *args) -> dict:
        """
        Sets market order of any type
        """
        order_result = self.exchange.market_open(*args)
        return handle_order_execution_results_hl(order_result, logger)
    
    def market_buy(self, coin:str, sz:float, slippage: float = DEFAULT_SLIPPAGE, price: Optional[float] = None) -> dict:
        return self._market_order(coin, True, sz, price, slippage)
    
    def market_sell(self, coin:str, sz:float, slippage: float = DEFAULT_SLIPPAGE, price: Optional[float] = None) -> dict:
        return self._market_order(coin, False, sz, price, slippage)

    def _limit_order(self, *args) -> dict:
        """
        Sets limit order of any type
        """
        order_result = self.exchange.order(*args)
        return handle_order_execution_results_hl(order_result, logger)
    
    def limit_buy(self, coin:str, sz: float, price: float, order_type={"limit": {"tif": "Gtc"}}) -> dict:
        return self._limit_order(coin, True, sz, price, order_type)
    
    def limit_sell(self, coin:str, sz: float, price: float, order_type={"limit": {"tif": "Gtc"}}) -> dict:
        return self._limit_order(coin, False, sz, price, order_type)

    def stop_order(self, coin:str):
        order_result = self.exchange.market_close(coin) 
        return handle_order_execution_results_hl(order_result, logger)

    def update_leverage(self, leverage: int, coin: str, is_cross_origin=True):
        self.exchange.update_leverage(leverage, coin, is_cross_origin)
        
    def load_depth(self, coin: str):
        res = self.info.l2_snapshot(coin=coin)
        bids = res["levels"][0]
        asks = res["levels"][1]

        return {
            "bids": bids,
            "asks": asks
        }
    
    def cancel_order(self, coin: str, oid: int):
        self.exchange.cancel(coin, oid)
        logger.info(f"order #{oid} canceled")

    def cancel_all_orders(self):
        open_orders = self.info.open_orders(self.address)
        for open_order in open_orders:
            self.cancel_order(open_order["coin"], open_order["oid"])


    def withdraw(self):
        pass
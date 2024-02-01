import os 
import logging
from v4_client_py.clients import CompositeClient, IndexerClient
from v4_client_py.clients.constants import Network


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DyDx:
    def __init__(self, mainnet=False) -> None:
        # if create_acc:
        #     self.generate_account()
        # else:
        #     self.get_account()
        
        if mainnet:
            self.ix_client = IndexerClient(Network.mainnet())
            self.comp_client = CompositeClient(Network.mainnet())

        else:
            # self.ix_client = IndexerClient(Network.testnet())
            self.comp_client = CompositeClient(Network.testnet())

    def get_depth(self, coin: str) -> dict:
        symbol = f"{coin}-USD"
        return self.comp_client.indexer_client.markets.get_perpetual_market_orderbook(symbol).data
    

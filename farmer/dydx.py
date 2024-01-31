from dotenv import load_dotenv 
import os 
import logging

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DyDx:
    def __init__(self) -> None:
        # self.seed_phrase = os.getenv("DYDX_ACCOUNT_SEED")

        # self.wallet = LocalWallet.from_mnemonic(self.seed_phrase)
        # self.private_key = self.wallet.signer().private_key_hex 
        
        # self.public_key = self.wallet.public_key().public_key_hex
        # self.address = self.wallet.address()

        # logger.info(f"Current public key: {self.public_key}, Current address: {self.address}")
        pass 


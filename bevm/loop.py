import time
from eth.db.atomic import AtomicDB
from eth.db.backends.level import LevelDB
from bevm.fetch import Fetcher


MAX_BLOCK_PER_FETCH = 1000


class Looper:
    def __init__(self, db_path=None):
        self.db = LevelDB(db_path) if db_path is not None else AtomicDB()

    def run_forever(self, rpc, contract, origin_block, required_confirmations):
        fetcher = Fetcher(rpc, contract)
        while True:
            start_block = None  # self.db.get_next_block()
            if start_block is None:
                start_block = origin_block
            end_block = min(
                start_block + MAX_BLOCK_PER_FETCH - 1,
                fetcher.block_number - required_confirmations,
            )
            if end_block < start_block:
                time.sleep(0.5)
                continue
            else:
                yield fetcher.fetch(start_block, end_block)
                # self.db.set_next_block(end_block + 1)

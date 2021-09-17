from eth.db.atomic import AtomicDB
from eth.db.backends.level import LevelDB
from eth.db.account import AccountDB
from rlp.sedes import big_endian_int
from bevm.block import Block
from bevm.action import rlp_decode_action


ACTION_COUNT = b'BEVM:ACTION_COUNT'


def block_key(blockno):
    return 'BEVM:BLOCK_KEY_{}'.format(blockno).encode()


class DB:
    def __init__(self, db_path=None):
        self.db = LevelDB(db_path) if db_path is not None else AtomicDB()
        if not self.db.exists(ACTION_COUNT):
            block0 = Block.default()
            block0hash = block0.hash()
            self.db.set(block0hash, block0.rlp_encode())
            self.db.set(block_key(0), block0hash)
            self.db.set(ACTION_COUNT, big_endian_int.serialize(0))

    @property
    def action_count(self):
        return big_endian_int.deserialize(self.db.get(ACTION_COUNT))

    def push_action(self, action):
        txhash = action.hash()
        self.db.set(txhash, action.rlp_encode())
        return txhash

    def push_block(self, block):
        action_count = self.action_count
        blockhash = block.hash()
        self.db.set(blockhash, block.rlp_encode())
        self.db.set(block_key(action_count + 1), blockhash)
        self.db.set(ACTION_COUNT, big_endian_int.serialize(action_count + 1))
        return blockhash, action_count + 1

    def get_state_db(self, state_root):
        return AccountDB(self.db, state_root)

    def get_lastest_block(self):
        return self.get_block_by_blockno(self.action_count)

    def get_block_by_blockno(self, blockno):
        return self.get_block_by_blockhash(self.db.get(block_key(blockno)))

    def get_block_by_blockhash(self, blockhash):
        return Block.rlp_decode(self.db.get(blockhash))

    def get_action_by_txhash(self, txhash):
        return rlp_decode_action(self.db.get(txhash))

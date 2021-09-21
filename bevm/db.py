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

    @property
    def block_count(self):
        return self.action_count

    def push_block(self, block, action):
        action_count = self.action_count
        actionhash = action.hash()
        blockhash = block.hash()
        assert block.action_hash == actionhash
        self.db.set(actionhash, action.rlp_encode())
        self.db.set(blockhash, block.rlp_encode())
        self.db.set(block_key(action_count + 1), blockhash)
        self.db.set(ACTION_COUNT, big_endian_int.serialize(action_count + 1))

    def get_state_db_by_root(self, state_root):
        return AccountDB(self.db, state_root)

    def get_latest_state_db(self):
        return self.get_state_db_by_root(self.get_latest_block().state_root)

    def get_latest_block(self):
        return self.get_block_by_blockno(self.action_count)

    def get_block_by_blockno(self, blockno):
        return self.get_block_by_hash(self.db.get(block_key(blockno)))

    def get_block_by_hash(self, blockhash):
        return Block.rlp_decode(self.db.get(blockhash))

    def get_action_by_hash(self, actionhash):
        return rlp_decode_action(self.db.get(actionhash))

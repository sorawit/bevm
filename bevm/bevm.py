from eth.db.atomic import AtomicDB
from eth.db.backends.level import LevelDB
from eth.db.account import AccountDB
from eth.db.hash_trie import HashTrie
from eth.vm.execution_context import ExecutionContext
from eth.vm.forks.berlin.state import BerlinState
from eth.constants import BLANK_ROOT_HASH
from bevm.block import Block


STATE_ROOT = b'BEVM_STATE_ROOT'
ACTION_COUNT = b'BEVM_ACTION_COUNT'
MIN_GAS_PRICE = b'BEVM_MIN_GAS_PRICE'

ZERO_ADDRESS = b'\x00' * 20


class BEVM:
    def __init__(self, db, chain_id=494):
        self.db = db
        self.chain_id = chain_id

    @property
    def action_count(self):
        return self.db.action_count

    # def _update_state_root(self, state_root):
    #     db = HashTrie(self.db)
    #     db.set(STATE_ROOT, state_root)

    # def _increase_action_count(self):
    #     db = HashTrie(self.db)
    #     db.set(ACTION_COUNT, (self.action_count + 1).to_bytes(8, 'big'))

    def get_balance(self, account):
        return self.db.get_latest_state_db().get_balance(account)

    def get_nonce(self, account):
        return self.db.get_latest_state_db().get_nonce(account)

    def get_storage_at(self, address, slot):
        return self.db.get_latest_state_db().get_storage(address, slot)

    def get_code(self, address):
        return self.db.get_latest_state_db().get_code(address)

    # def apply_min_gas_price(self, min_gas_price):
    #     '''Perform global min gas price update.'''
    #     db = HashTrie(self.db)
    #     db.set(MIN_GAS_PRICE, min_gas_price.to_bytes(8, 'big'))
    #     self._increase_action_count()

    def apply_mint(self, action):
        latest_block = self.db.get_latest_block()
        db = self.db.get_latest_state_db()
        db.lock_changes()
        db.set_balance(action.to, db.get_balance(action.to) + action.value)
        db.commit(db.record())
        db.persist()
        self.db.push_block(Block(
            timestamp=0,
            prev_block_hash=latest_block.hash(),
            action_hash=action.hash(),
            min_gas_price=latest_block.min_gas_price,
            state_root=db.make_state_root(),
        ), action)

    def apply_transaction(self, action):
        latest_block = self.db.get_latest_block()
        ctx = ExecutionContext(
            ZERO_ADDRESS,
            0,
            self.db.action_count + 1,
            0,
            0,
            [],
            self.chain_id,
        )
        state = BerlinState(self.db.db, ctx, latest_block.state_root)
        state.lock_changes()
        # TODO: Check min gas price
        # TODO: Handle revert case
        state.apply_transaction(action.as_signed_tx())
        state.commit(state.snapshot())
        state.persist()
        self.db.push_block(Block(
            timestamp=0,
            prev_block_hash=latest_block.hash(),
            action_hash=action.hash(),
            min_gas_price=latest_block.min_gas_price,
            state_root=state.state_root,
        ), action)

    # def try_transaction(self, timestamp, unsigned_tx):
    #     latest_block = self.db.get_latest_block()
    #     ctx = ExecutionContext(ZERO_ADDRESS, timestamp, self.action_count, 0, 0, [], self.chain_id)
    #     state = BerlinState(self.db.db, ctx, latest_block.state_root)
    #     snapshot = state.snapshot()
    #     try:
    #         return state.apply_transaction(unsigned_tx)
    #     finally:
    #         state.revert(snapshot)

from eth.db.atomic import AtomicDB
from eth.db.backends.level import LevelDB
from eth.db.account import AccountDB
from eth.db.hash_trie import HashTrie
from eth.vm.execution_context import ExecutionContext
from eth.vm.spoof import SpoofTransaction
from eth.vm.forks.berlin.state import BerlinState
from eth.vm.forks.berlin.transactions import BerlinTransactionBuilder
from eth.constants import BLANK_ROOT_HASH


STATE_ROOT = b'BEVM_STATE_ROOT'
MIN_GAS_PRICE = b'BEVM_MIN_GAS_PRICE'
ACTION_COUNT = b'BEVM_ACTION_COUNT'
ZERO_ADDRESS = b'\x00' * 20


class BEVM:
    def __init__(self, db_path=None, chain_id=494, default_min_gas_price=10**9):
        '''Initialize a new BEVM instance.'''
        self.db = LevelDB(db_path) if db_path is not None else AtomicDB()
        self.chain_id = chain_id
        self.default_min_gas_price = default_min_gas_price

    @property
    def state_root(self):
        '''Return the currently stored state root.'''
        db = HashTrie(self.db)
        return db.get(STATE_ROOT) if db.exists(STATE_ROOT) else BLANK_ROOT_HASH

    @property
    def min_gas_price(self):
        '''Return the current gas price.'''
        db = HashTrie(self.db)
        return (
            int.from_bytes(db.get(MIN_GAS_PRICE), 'big')
            if db.exists(MIN_GAS_PRICE) else self.default_min_gas_price
        )

    @property
    def action_count(self):
        '''Return the total number of mutate actions to this system.'''
        db = HashTrie(self.db)
        return int.from_bytes(db.get(ACTION_COUNT), 'big') if db.exists(ACTION_COUNT) else 0

    def _update_state_root(self, state_root):
        db = HashTrie(self.db)
        db.set(STATE_ROOT, state_root)

    def _increase_action_count(self):
        db = HashTrie(self.db)
        db.set(ACTION_COUNT, (self.action_count + 1).to_bytes(8, 'big'))

    def get_balance(self, account):
        '''Return the balance of the given account.'''
        db = AccountDB(self.db, self.state_root)
        return db.get_balance(account)

    def apply_min_gas_price(self, min_gas_price):
        '''Perform global min gas price update.'''
        db = HashTrie(self.db)
        db.set(MIN_GAS_PRICE, min_gas_price.to_bytes(8, 'big'))
        self._increase_action_count()

    def apply_mint(self, account, amount):
        '''Perform native token mining for the given account.'''
        db = AccountDB(self.db, self.state_root)
        db.lock_changes()
        db.set_balance(account, db.get_balance(account) + amount)
        db.commit(db.record())
        db.persist()
        self._update_state_root(db.make_state_root())
        self._increase_action_count()

    def apply_transaction(self, timestamp, nonce, gas_price, gas, to, value, data, v, r, s):
        '''Apply transaction to the BEVM and update the state root + action count.'''
        ctx = ExecutionContext(
            ZERO_ADDRESS, timestamp, self.action_count,
            0, 0, [], self.chain_id,
        )
        tx = BerlinTransactionBuilder.new_transaction(
            nonce, gas_price, gas, to, value, data, v, r, s,
        )
        state = BerlinState(self.db, ctx, self.state_root)
        state.lock_changes()
        # TODO: Check min gas price
        # TODO: Handle revert case
        state.apply_transaction(tx)
        state.commit(state.snapshot())
        state.persist()
        self._update_state_root(state.state_root)
        self._increase_action_count()

    def try_transaction(self, timestamp, sender, gas_price, gas, to, value, data):
        '''Try applying the transaction the BEVM but discard all state changes.'''
        ctx = ExecutionContext(
            ZERO_ADDRESS, timestamp, self.action_count,
            0, 0, [], self.chain_id,
        )
        state = BerlinState(self.db, ctx, self.state_root)
        snapshot = state.snapshot()
        try:
            nonce = state.get_nonce(sender)
            tx = SpoofTransaction(BerlinTransactionBuilder.create_unsigned_transaction(
                nonce=nonce, gas_price=gas_price, gas=gas, to=to, value=value, data=data,
            ), from_=sender)
            return state.apply_transaction(tx)
        finally:
            state.revert(snapshot)

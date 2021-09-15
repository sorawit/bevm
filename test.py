from eth.db.atomic import AtomicDB
from eth.db.backends.level import LevelDB
from eth.db.journal import JournalDB
from eth.vm.state import BaseState, BaseTransactionExecutor
from eth.vm.forks.berlin.state import BerlinState
from eth.vm.forks.berlin.transactions import BerlinTransactionBuilder
from eth.vm.execution_context import ExecutionContext
from eth.constants import BLANK_ROOT_HASH
from eth._utils.transactions import extract_transaction_sender

from eth_account.account import Account


ZERO_ADDRESS = b'\x00' * 20
ONE_ADDRESS = b'\x11' * 20


def main():
    a = Account.create('ACCOUNT_A')
    print(a.address)
    sig = Account.sign_transaction({
        'chainId': 494,
        'data': b'hello, world',
        'nonce': 0,
        'to': ONE_ADDRESS,
        'gas': 30000,
        'gasPrice': 1,
        'value': 10**17,
    }, a.key)
    lv = LevelDB('./db/testx.db')
    # db = AtomicDB(lv)
    db = AtomicDB()
    cx = ExecutionContext(ZERO_ADDRESS, 1, 1, 1, 0, [], 494)
    st = BerlinState(db, cx, BLANK_ROOT_HASH)
    # st = BerlinState(db, cx, b'\xba,&8\xb3\xe2:\x85T\x99\xaa\xf2\x07\xc4M\x96-\xec\xa8\xbbrP\xe4[\xcf\x1d\xc9..jYI')
    tx = BerlinTransactionBuilder.new_transaction(
        nonce=0,
        gas_price=1,
        gas=30000,
        to=ONE_ADDRESS,
        value=10**17,
        data=b'hello, world',
        v=sig.v,
        r=sig.r,
        s=sig.s,
    )
    sender = extract_transaction_sender(tx)
    print('0x'+sender.hex())
    st.set_balance(sender, 10**18)
    comp = st.apply_transaction(tx)
    print(comp.get_gas_used(), comp.get_gas_remaining(), comp.return_data)
    # print(st.account_exists(B_ADDRESS))
    print(st.get_balance(sender))
    print(st.get_balance(ONE_ADDRESS))
    st.commit(st.snapshot())
    st.persist()
    x = st.state_root
    st = BerlinState(db, cx, x)
    print(st.get_balance(ONE_ADDRESS))
    print(x)
    # db = JournalDB(AtomicDB())
    # db[123] = 456
    # print(db.exists(123))
    # db.persist()
    # db.reset()
    # print(db.exists(123))


if __name__ == '__main__':
    main()

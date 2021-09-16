from eth.vm.forks.berlin.transactions import BerlinTransactionBuilder
from eth.vm.spoof import SpoofTransaction


def build_signed_tx(nonce, gas_price, gas, to, value, data, v, r, s):
    return BerlinTransactionBuilder.new_transaction(
        nonce, gas_price, gas, to, value, data, v, r, s,
    )


def build_spoof_tx(sender, nonce, gas_price, gas, to, value, data):
    return SpoofTransaction(BerlinTransactionBuilder.create_unsigned_transaction(
        nonce=nonce, gas_price=gas_price, gas=gas, to=to, value=value, data=data,
    ), from_=sender)

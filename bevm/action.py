from dataclasses import dataclass
from rlp import encode, decode
from rlp.sedes import big_endian_int
from eth.vm.forks.berlin.transactions import BerlinTransactionBuilder
from eth_hash.auto import keccak

from bevm.hashable import Hashable

MAGIC_SIZE = 4
MINT_ACTION_MAGIC = keccak(b'MINT_ACTION')[:MAGIC_SIZE]


@dataclass
class MintAction(Hashable):
    to: bytes
    value: int

    def rlp_encode(self):
        return MINT_ACTION_MAGIC + encode((self.to, big_endian_int.serialize(self.value)))

    @classmethod
    def rlp_decode(cls, data):
        assert data[:MAGIC_SIZE] == MINT_ACTION_MAGIC
        (to, value) = decode(data[MAGIC_SIZE:])
        return cls(to, big_endian_int.deserialize(value))


MAGIC_MAPPING = {
    MINT_ACTION_MAGIC: MintAction,
}


@dataclass
class TransactionAction(Hashable):
    nonce: int
    gas_price: int
    gas: int
    to: bytes
    value: int
    data: bytes
    v: int
    r: int
    s: int

    def as_signed_tx(self):
        return BerlinTransactionBuilder.new_transaction(
            self.nonce, self.gas_price, self.gas, self.to, self.value, self.data,
            self.v, self.r, self.s,
        )

    def rlp_encode(self):
        res = encode((
            big_endian_int.serialize(self.nonce),
            big_endian_int.serialize(self.gas_price),
            big_endian_int.serialize(self.gas),
            self.to,
            big_endian_int.serialize(self.value),
            self.data,
            big_endian_int.serialize(self.v),
            big_endian_int.serialize(self.r),
            big_endian_int.serialize(self.s),
        ))
        assert res[:MAGIC_SIZE] not in MAGIC_MAPPING.keys()
        return res

    @classmethod
    def rlp_decode(cls, data):
        assert data[:MAGIC_SIZE] not in MAGIC_MAPPING.keys()
        (nonce, gas_price, gas, to, value, data, v, r, s) = decode(data)
        return cls(
            big_endian_int.deserialize(nonce),
            to,
            big_endian_int.deserialize(value),
            big_endian_int.deserialize(gas),
            big_endian_int.deserialize(gas_price),
            big_endian_int.deserialize(v),
            big_endian_int.deserialize(r),
            big_endian_int.deserialize(s),
            data,
        )


def rlp_decode_action(data):
    magic = data[:MAGIC_SIZE]
    return MAGIC_MAPPING.get(magic, TransactionAction).rlp_decode(data)
